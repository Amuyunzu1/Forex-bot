"""
Trade execution module.
Executes trades based on monitored price conditions.
"""

import logging
import threading
import time
from datetime import datetime
from typing import Dict, List, Optional, Any

from core.broker import BrokerConnection, OrderType
from core.monitor import PriceMonitor
from core.trade import TradeInstruction, ActiveTrade


class TradeExecutor:
    """
    Class for executing trades based on monitored price conditions.
    """
    
    def __init__(self, broker: BrokerConnection, monitor: PriceMonitor, max_retries: int = 3, retry_delay: float = 1.0):
        """
        Initialize trade executor.
        
        Args:
            broker (BrokerConnection): Broker connection
            monitor (PriceMonitor): Price monitor
            max_retries (int, optional): Maximum retry attempts for trade execution
            retry_delay (float, optional): Delay between retry attempts in seconds
        """
        self.logger = logging.getLogger("hunter_bot.executor")
        self.broker = broker
        self.monitor = monitor
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        
        # Store trade instructions and active trades
        self.trade_instructions = []  # List of pending trade instructions
        self.active_trades = []  # List of active trades
        
        # Lock for thread-safe access to trade lists
        self.trade_lock = threading.RLock()
        
        # Register callbacks with monitor
        self.monitor.register_entry_callback(self._on_entry_condition)
        self.monitor.register_exit_callback(self._on_exit_condition)
        self.monitor.register_sl_callback(self._on_sl_condition)
    
    def add_trade_instruction(self, instruction: Dict[str, Any]) -> bool:
        """
        Add a new trade instruction.
        
        Args:
            instruction (Dict[str, Any]): Trade instruction details
                {
                    "symbol": str,
                    "entry_price": float,
                    "exit_price": float,
                    "stop_loss": float,
                    "lot_size": float,
                    "direction": str ("buy" or "sell"),
                    "comment": str (optional)
                }
                
        Returns:
            bool: True if instruction added successfully, False otherwise
        """
        # Validate instruction
        required_fields = ["symbol", "entry_price", "exit_price", "stop_loss", "lot_size"]
        for field in required_fields:
            if field not in instruction:
                self.logger.error(f"Missing required field in trade instruction: {field}")
                return False
        
        # Validate numeric fields
        numeric_fields = ["entry_price", "exit_price", "stop_loss", "lot_size"]
        for field in numeric_fields:
            try:
                instruction[field] = float(instruction[field])
            except (ValueError, TypeError):
                self.logger.error(f"Invalid numeric value for {field}: {instruction[field]}")
                return False
        
        # Set default direction if not provided
        if "direction" not in instruction:
            # Determine direction based on entry and exit prices
            if instruction["exit_price"] > instruction["entry_price"]:
                instruction["direction"] = "buy"
            else:
                instruction["direction"] = "sell"
        
        # Validate direction
        if instruction["direction"].lower() not in ["buy", "sell"]:
            self.logger.error(f"Invalid direction: {instruction['direction']}")
            return False
        
        # Create TradeInstruction object
        trade_instruction = TradeInstruction(
            symbol=instruction["symbol"],
            entry_price=instruction["entry_price"],
            exit_price=instruction["exit_price"],
            stop_loss=instruction["stop_loss"],
            lot_size=instruction["lot_size"],
            direction=instruction["direction"].lower(),
            comment=instruction.get("comment", "Hunter Bot")
        )
        
        # Add to pending instructions
        with self.trade_lock:
            self.trade_instructions.append(trade_instruction)
        
        # Add symbol to monitor
        self.monitor.add_symbol(instruction["symbol"])
        
        self.logger.info(f"Added trade instruction for {instruction['symbol']} at {instruction['entry_price']}")
        return True
    
    def remove_trade_instruction(self, instruction_id: int) -> bool:
        """
        Remove a trade instruction by ID.
        
        Args:
            instruction_id (int): ID of the instruction to remove
            
        Returns:
            bool: True if instruction removed successfully, False otherwise
        """
        with self.trade_lock:
            for i, instruction in enumerate(self.trade_instructions):
                if instruction.id == instruction_id:
                    # Check if we need to keep monitoring the symbol
                    symbol = instruction.symbol
                    remove_symbol = True
                    
                    # Check if symbol is used in other instructions
                    for other_instruction in self.trade_instructions:
                        if other_instruction.id != instruction_id and other_instruction.symbol == symbol:
                            remove_symbol = False
                            break
                    
                    # Check if symbol is used in active trades
                    for trade in self.active_trades:
                        if trade.symbol == symbol:
                            remove_symbol = False
                            break
                    
                    # Remove instruction
                    self.trade_instructions.pop(i)
                    
                    # Remove symbol from monitoring if not used elsewhere
                    if remove_symbol:
                        self.monitor.remove_symbol(symbol)
                    
                    self.logger.info(f"Removed trade instruction #{instruction_id}")
                    return True
        
        self.logger.warning(f"Trade instruction #{instruction_id} not found")
        return False
    
    def get_trade_instructions(self) -> List[Dict[str, Any]]:
        """
        Get all pending trade instructions.
        
        Returns:
            List[Dict[str, Any]]: List of trade instruction dictionaries
        """
        with self.trade_lock:
            return [instruction.to_dict() for instruction in self.trade_instructions]
    
    def get_active_trades(self) -> List[Dict[str, Any]]:
        """
        Get all active trades.
        
        Returns:
            List[Dict[str, Any]]: List of active trade dictionaries
        """
        with self.trade_lock:
            return [trade.to_dict() for trade in self.active_trades]
    
    def cancel_all_instructions(self) -> int:
        """
        Cancel all pending trade instructions.
        
        Returns:
            int: Number of instructions cancelled
        """
        with self.trade_lock:
            count = len(self.trade_instructions)
            self.trade_instructions = []
            
            # Update symbol monitoring
            self._update_monitored_symbols()
            
            self.logger.info(f"Cancelled {count} trade instructions")
            return count
    
    def close_all_trades(self) -> int:
        """
        Close all active trades.
        
        Returns:
            int: Number of trades closed successfully
        """
        closed_count = 0
        
        with self.trade_lock:
            for trade in list(self.active_trades):
                if self._close_trade(trade.ticket):
                    closed_count += 1
        
        self.logger.info(f"Closed {closed_count} trades")
        return closed_count
    
    def close_trade(self, trade_id: int) -> bool:
        """
        Close a specific trade by ID.
        
        Args:
            trade_id (int): ID of trade to close
            
        Returns:
            bool: True if trade closed successfully, False otherwise
        """
        return self._close_trade(trade_id)
    
    def _close_trade(self, ticket: int) -> bool:
        """
        Close a trade by ticket.
        
        Args:
            ticket (int): Ticket of trade to close
            
        Returns:
            bool: True if trade closed successfully, False otherwise
        """
        # Find trade in active trades
        trade_to_remove = None
        with self.trade_lock:
            for trade in self.active_trades:
                if trade.ticket == ticket:
                    trade_to_remove = trade
                    break
        
        if trade_to_remove is None:
            self.logger.warning(f"Trade with ticket {ticket} not found")
            return False
        
        # Close position
        for attempt in range(1, self.max_retries + 1):
            if self.broker.close_position(ticket):
                with self.trade_lock:
                    self.active_trades.remove(trade_to_remove)
                    
                    # Update symbol monitoring
                    self._update_monitored_symbols()
                
                self.logger.info(f"Closed trade #{ticket} for {trade_to_remove.symbol}")
                return True
            
            self.logger.warning(f"Failed to close trade #{ticket}, attempt {attempt}/{self.max_retries}")
            time.sleep(self.retry_delay)
        
        self.logger.error(f"Failed to close trade #{ticket} after {self.max_retries} attempts")
        return False
    
    def _update_monitored_symbols(self) -> None:
        """Update the list of symbols to monitor based on instructions and active trades."""
        # Collect all symbols that need monitoring
        symbols_to_monitor = set()
        
        with self.trade_lock:
            # Add symbols from instructions
            for instruction in self.trade_instructions:
                symbols_to_monitor.add(instruction.symbol)
            
            # Add symbols from active trades
            for trade in self.active_trades:
                symbols_to_monitor.add(trade.symbol)
        
        # Update monitor's symbols
        current_symbols = set(self.monitor.symbols_to_monitor)
        
        # Add new symbols
        for symbol in symbols_to_monitor - current_symbols:
            self.monitor.add_symbol(symbol)
        
        # Remove unused symbols
        for symbol in current_symbols - symbols_to_monitor:
            self.monitor.remove_symbol(symbol)
    
    def _on_entry_condition(self, symbol: str, price: Dict[str, float]) -> None:
        """
        Callback for when entry condition is met.
        
        Args:
            symbol (str): Symbol that met entry condition
            price (Dict[str, float]): Current price data
        """
        instructions_to_execute = []
        
        # Find matching instructions
        with self.trade_lock:
            for instruction in list(self.trade_instructions):
                if instruction.symbol != symbol:
                    continue
                
                # Check entry condition
                entry_price = instruction.entry_price
                direction = instruction.direction
                
                if (direction == "buy" and price["ask"] <= entry_price) or \
                   (direction == "sell" and price["bid"] >= entry_price):
                    instructions_to_execute.append(instruction)
        
        # Execute trades
        for instruction in instructions_to_execute:
            self._execute_trade(instruction, price)
    
    def _on_exit_condition(self, symbol: str, price: Dict[str, float], position: Dict[str, Any]) -> None:
        """
        Callback for when exit condition (take profit) is met.
        
        Args:
            symbol (str): Symbol that met exit condition
            price (Dict[str, float]): Current price data
            position (Dict[str, Any]): Position data
        """
        ticket = position["ticket"]
        self.logger.info(f"Take profit reached for {symbol} (#{ticket}), closing position")
        self._close_trade(ticket)
    
    def _on_sl_condition(self, symbol: str, price: Dict[str, float], position: Dict[str, Any]) -> None:
        """
        Callback for when stop loss condition is met.
        
        Args:
            symbol (str): Symbol that met stop loss condition
            price (Dict[str, float]): Current price data
            position (Dict[str, Any]): Position data
        """
        ticket = position["ticket"]
        self.logger.info(f"Stop loss reached for {symbol} (#{ticket}), closing position")
        self._close_trade(ticket)
    
    def _execute_trade(self, instruction: TradeInstruction, price: Dict[str, float]) -> bool:
        """
        Execute a trade based on instruction.
        
        Args:
            instruction (TradeInstruction): Trade instruction to execute
            price (Dict[str, float]): Current price data
            
        Returns:
            bool: True if trade executed successfully, False otherwise
        """
        self.logger.info(f"Executing trade for {instruction.symbol} at {price}")
        
        # Determine order type
        order_type = OrderType.BUY if instruction.direction == "buy" else OrderType.SELL
        
        # Execute market order
        for attempt in range(1, self.max_retries + 1):
            ticket = self.broker.place_market_order(
                symbol=instruction.symbol,
                order_type=order_type,
                lot_size=instruction.lot_size,
                stop_loss=instruction.stop_loss,
                take_profit=instruction.exit_price,
                comment=instruction.comment
            )
            
            if ticket:
                # Create active trade record
                trade = ActiveTrade(
                    ticket=ticket,
                    symbol=instruction.symbol,
                    entry_price=price["ask"] if order_type == OrderType.BUY else price["bid"],
                    exit_price=instruction.exit_price,
                    stop_loss=instruction.stop_loss,
                    lot_size=instruction.lot_size,
                    direction=instruction.direction,
                    comment=instruction.comment,
                    entry_time=datetime.now()
                )
                
                # Add to active trades and remove from instructions
                with self.trade_lock:
                    self.active_trades.append(trade)
                    self.trade_instructions.remove(instruction)
                
                self.logger.info(f"Trade executed successfully, ticket #{ticket}")
                return True
            
            self.logger.warning(f"Failed to execute trade for {instruction.symbol}, attempt {attempt}/{self.max_retries}")
            time.sleep(self.retry_delay)
        
        self.logger.error(f"Failed to execute trade for {instruction.symbol} after {self.max_retries} attempts")
        return False