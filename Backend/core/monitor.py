"""
Price monitoring module.
Monitors price movements and detects entry/exit conditions.
"""

import logging
import threading
import time
from typing import Dict, List, Optional, Callable, Any

from core.broker import BrokerConnection


class PriceMonitor:
    """
    Class for monitoring price movements and detecting trading conditions.
    """
    
    def __init__(self, broker: BrokerConnection, update_interval: float = 1.0):
        """
        Initialize price monitor.
        
        Args:
            broker (BrokerConnection): Broker connection
            update_interval (float, optional): Update interval in seconds
        """
        self.logger = logging.getLogger("hunter_bot.monitor")
        self.broker = broker
        self.update_interval = update_interval
        self.symbols_to_monitor = set()
        self.price_data = {}  # Store latest prices
        self._monitoring_thread = None
        self._stop_monitoring = threading.Event()
        
        # Callbacks for price events
        self.entry_callbacks = []
        self.exit_callbacks = []
        self.sl_callbacks = []
    
    def add_symbol(self, symbol: str) -> bool:
        """
        Add symbol to monitoring list.
        
        Args:
            symbol (str): Symbol to monitor
            
        Returns:
            bool: True if added successfully, False otherwise
        """
        if not self.broker.is_connected():
            self.logger.error("Cannot add symbol, broker not connected")
            return False
        
        # Check if symbol is valid
        price = self.broker.get_price(symbol)
        if price is None:
            self.logger.error(f"Cannot add invalid symbol: {symbol}")
            return False
        
        self.symbols_to_monitor.add(symbol)
        self.price_data[symbol] = price
        self.logger.info(f"Added symbol to monitor: {symbol}")
        return True
    
    def remove_symbol(self, symbol: str) -> bool:
        """
        Remove symbol from monitoring list.
        
        Args:
            symbol (str): Symbol to remove
            
        Returns:
            bool: True if removed successfully, False otherwise
        """
        if symbol in self.symbols_to_monitor:
            self.symbols_to_monitor.remove(symbol)
            if symbol in self.price_data:
                del self.price_data[symbol]
            self.logger.info(f"Removed symbol from monitoring: {symbol}")
            return True
        
        self.logger.warning(f"Symbol not in monitoring list: {symbol}")
        return False
    
    def get_price(self, symbol: str) -> Optional[Dict[str, float]]:
        """
        Get current price for a symbol.
        
        Args:
            symbol (str): Symbol to get price for
            
        Returns:
            Optional[Dict[str, float]]: Dictionary with bid and ask prices, or None if error
        """
        if not self.broker.is_connected():
            self.logger.error("Cannot get price, broker not connected")
            return None
        
        # Use cached price if available and recent
        if symbol in self.price_data:
            current_time = time.time()
            # Consider price data valid if it's less than 5 seconds old
            if "time" not in self.price_data[symbol] or current_time - self.price_data[symbol]["time"] < 5:
                return self.price_data[symbol]
        
        # Get fresh price from broker
        price = self.broker.get_price(symbol)
        if price:
            self.price_data[symbol] = price
        
        return price
    
    def start_monitoring(self) -> bool:
        """
        Start price monitoring thread.
        
        Returns:
            bool: True if started successfully, False otherwise
        """
        if not self.broker.is_connected():
            self.logger.error("Cannot start monitoring, broker not connected")
            return False
        
        if self._monitoring_thread and self._monitoring_thread.is_alive():
            self.logger.warning("Monitoring already running")
            return True
        
        self._stop_monitoring.clear()
        self._monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self._monitoring_thread.start()
        self.logger.info("Price monitoring started")
        return True
    
    def stop_monitoring(self) -> bool:
        """
        Stop price monitoring thread.
        
        Returns:
            bool: True if stopped successfully, False otherwise
        """
        if not self._monitoring_thread or not self._monitoring_thread.is_alive():
            self.logger.warning("Monitoring not running")
            return True
        
        self._stop_monitoring.set()
        self._monitoring_thread.join(timeout=5.0)
        
        if self._monitoring_thread.is_alive():
            self.logger.error("Failed to stop monitoring thread")
            return False
        
        self.logger.info("Price monitoring stopped")
        return True
    
    def is_monitoring(self) -> bool:
        """
        Check if monitoring is active.
        
        Returns:
            bool: True if monitoring is active, False otherwise
        """
        return self._monitoring_thread is not None and self._monitoring_thread.is_alive()
    
    def register_entry_callback(self, callback: Callable[[str, float, Dict], None]) -> None:
        """
        Register callback for price entry condition.
        
        Args:
            callback: Function to call when entry condition is met
                     callback(symbol, price, instruction)
        """
        self.entry_callbacks.append(callback)
    
    def register_exit_callback(self, callback: Callable[[str, float, Dict], None]) -> None:
        """
        Register callback for price exit condition (take profit).
        
        Args:
            callback: Function to call when exit condition is met
                     callback(symbol, price, position)
        """
        self.exit_callbacks.append(callback)
    
    def register_sl_callback(self, callback: Callable[[str, float, Dict], None]) -> None:
        """
        Register callback for stop loss condition.
        
        Args:
            callback: Function to call when stop loss condition is met
                     callback(symbol, price, position)
        """
        self.sl_callbacks.append(callback)
    
    def check_entry_condition(self, symbol: str, instruction: Dict[str, Any]) -> bool:
        """
        Check if entry condition is met for a symbol.
        
        Args:
            symbol (str): Symbol to check
            instruction (Dict[str, Any]): Trade instruction
            
        Returns:
            bool: True if entry condition is met, False otherwise
        """
        price = self.get_price(symbol)
        if not price:
            return False
        
        entry_price = float(instruction["entry_price"])
        direction = instruction.get("direction", "buy").lower()
        
        # For buy orders, check if current ask price is less than or equal to entry price
        if direction == "buy" and price["ask"] <= entry_price:
            return True
        
        # For sell orders, check if current bid price is greater than or equal to entry price
        if direction == "sell" and price["bid"] >= entry_price:
            return True
        
        return False
    
    def check_exit_condition(self, symbol: str, position: Dict[str, Any]) -> bool:
        """
        Check if exit condition (take profit) is met for a position.
        
        Args:
            symbol (str): Symbol to check
            position (Dict[str, Any]): Position data
            
        Returns:
            bool: True if exit condition is met, False otherwise
        """
        price = self.get_price(symbol)
        if not price:
            return False
        
        take_profit = position.get("take_profit")
        if take_profit is None:
            return False
        
        position_type = position.get("type", "").lower()
        
        # For buy positions, check if current bid price is greater than or equal to take profit
        if position_type == "buy" and price["bid"] >= take_profit:
            return True
        
        # For sell positions, check if current ask price is less than or equal to take profit
        if position_type == "sell" and price["ask"] <= take_profit:
            return True
        
        return False
    
    def check_sl_condition(self, symbol: str, position: Dict[str, Any]) -> bool:
        """
        Check if stop loss condition is met for a position.
        
        Args:
            symbol (str): Symbol to check
            position (Dict[str, Any]): Position data
            
        Returns:
            bool: True if stop loss condition is met, False otherwise
        """
        price = self.get_price(symbol)
        if not price:
            return False
        
        stop_loss = position.get("stop_loss")
        if stop_loss is None:
            return False
        
        position_type = position.get("type", "").lower()
        
        # For buy positions, check if current bid price is less than or equal to stop loss
        if position_type == "buy" and price["bid"] <= stop_loss:
            return True
        
        # For sell positions, check if current ask price is greater than or equal to stop loss
        if position_type == "sell" and price["ask"] >= stop_loss:
            return True
        
        return False
    
    def _monitoring_loop(self) -> None:
        """Main monitoring loop that checks prices and triggers callbacks."""
        self.logger.info("Monitoring loop started")
        
        while not self._stop_monitoring.is_set():
            if not self.broker.is_connected():
                self.logger.error("Broker connection lost, stopping monitoring")
                break
            
            try:
                # Get open positions
                positions = self.broker.get_positions()
                position_symbols = set(pos["symbol"] for pos in positions)
                
                # Add position symbols to monitoring if not already there
                for symbol in position_symbols:
                    if symbol not in self.symbols_to_monitor:
                        self.add_symbol(symbol)
                
                # Check all monitored symbols
                for symbol in list(self.symbols_to_monitor):
                    # Update price
                    price = self.broker.get_price(symbol)
                    if price:
                        self.price_data[symbol] = price
                    else:
                        continue
                    
                    # Check entry conditions for pending instructions
                    for callback in self.entry_callbacks:
                        try:
                            callback(symbol, price)
                        except Exception as e:
                            self.logger.error(f"Error in entry callback: {e}")
                    
                    # Check take profit and stop loss for open positions
                    for position in positions:
                        if position["symbol"] != symbol:
                            continue
                        
                        # Check take profit
                        if self.check_exit_condition(symbol, position):
                            for callback in self.exit_callbacks:
                                try:
                                    callback(symbol, price, position)
                                except Exception as e:
                                    self.logger.error(f"Error in exit callback: {e}")
                        
                        # Check stop loss
                        if self.check_sl_condition(symbol, position):
                            for callback in self.sl_callbacks:
                                try:
                                    callback(symbol, price, position)
                                except Exception as e:
                                    self.logger.error(f"Error in stop loss callback: {e}")
            
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
            
            # Sleep for update interval
            time.sleep(self.update_interval)
        
        self.logger.info("Monitoring loop stopped")