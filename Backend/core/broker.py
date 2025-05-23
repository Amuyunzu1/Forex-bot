"""
Broker connection module.
Handles the connection to trading platforms.
"""

import logging
import time
from enum import Enum
from typing import Dict, List, Optional, Tuple, Union, Any

# Import MetaTrader5 with error handling
try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False


class OrderType(Enum):
    """Enum for order types."""
    BUY = 0
    SELL = 1


class BrokerConnection:
    """Class to handle connections to trading broker platforms."""
    
    def __init__(self, platform: str, server: str, login: int, password: str, path: str = None):
        """
        Initialize broker connection.
        
        Args:
            platform (str): Trading platform (MT5, cTrader, etc.)
            server (str): Broker server
            login (int): Account login
            password (str): Account password
            path (str, optional): Path to terminal executable
        """
        self.logger = logging.getLogger("hunter_bot.broker")
        self.platform = platform.upper()
        self.server = server
        
        try:
            self.login = int(login)
        except ValueError:
            self.login = login  # Some platforms might use string logins
            
        self.password = password
        self.path = path
        self._connected = False
        
        if self.platform == "MT5" and not MT5_AVAILABLE:
            self.logger.error("MetaTrader5 package not installed. Please install it with: pip install MetaTrader5")
            raise ImportError("MetaTrader5 package not installed")
    
    def connect(self) -> bool:
        """
        Connect to the broker platform.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        if self._connected:
            self.logger.warning("Already connected to broker")
            return True
        
        self.logger.info(f"Connecting to {self.platform} broker...")
        
        if self.platform == "MT5":
            return self._connect_mt5()
        else:
            self.logger.error(f"Unsupported platform: {self.platform}")
            return False
    
    def disconnect(self) -> bool:
        """
        Disconnect from the broker platform.
        
        Returns:
            bool: True if disconnection successful, False otherwise
        """
        if not self._connected:
            self.logger.warning("Not connected to broker")
            return True
        
        self.logger.info(f"Disconnecting from {self.platform}...")
        
        if self.platform == "MT5":
            return self._disconnect_mt5()
        else:
            self.logger.error(f"Unsupported platform: {self.platform}")
            return False
    
    def is_connected(self) -> bool:
        """
        Check if connected to broker.
        
        Returns:
            bool: True if connected, False otherwise
        """
        if self.platform == "MT5" and MT5_AVAILABLE:
            return mt5.terminal_info() is not None and self._connected
        return self._connected
    
    def get_price(self, symbol: str) -> Optional[Dict[str, float]]:
        """
        Get current price for a symbol.
        
        Args:
            symbol (str): Symbol to get price for
            
        Returns:
            Optional[Dict[str, float]]: Dictionary with bid and ask prices, or None if error
        """
        if not self.is_connected():
            self.logger.error("Not connected to broker")
            return None
        
        if self.platform == "MT5":
            return self._get_price_mt5(symbol)
        else:
            self.logger.error(f"Unsupported platform: {self.platform}")
            return None
    
    def place_market_order(
        self, 
        symbol: str, 
        order_type: OrderType, 
        lot_size: float, 
        stop_loss: float = None, 
        take_profit: float = None,
        comment: str = "Hunter Bot"
    ) -> Optional[int]:
        """
        Place a market order.
        
        Args:
            symbol (str): Symbol to trade
            order_type (OrderType): Order type (BUY or SELL)
            lot_size (float): Lot size
            stop_loss (float, optional): Stop loss price
            take_profit (float, optional): Take profit price
            comment (str, optional): Order comment
            
        Returns:
            Optional[int]: Order ticket number if successful, None if failed
        """
        if not self.is_connected():
            self.logger.error("Not connected to broker")
            return None
        
        self.logger.info(f"Placing {order_type.name} market order for {symbol}, lot size: {lot_size}")
        
        if self.platform == "MT5":
            return self._place_market_order_mt5(
                symbol, order_type, lot_size, stop_loss, take_profit, comment
            )
        else:
            self.logger.error(f"Unsupported platform: {self.platform}")
            return None
    
    def close_position(self, ticket: int) -> bool:
        """
        Close a position by ticket.
        
        Args:
            ticket (int): Ticket number of position to close
            
        Returns:
            bool: True if position closed successfully, False otherwise
        """
        if not self.is_connected():
            self.logger.error("Not connected to broker")
            return False
        
        self.logger.info(f"Closing position with ticket: {ticket}")
        
        if self.platform == "MT5":
            return self._close_position_mt5(ticket)
        else:
            self.logger.error(f"Unsupported platform: {self.platform}")
            return False
    
    def modify_position(
        self, 
        ticket: int, 
        stop_loss: float = None, 
        take_profit: float = None
    ) -> bool:
        """
        Modify a position's stop loss and take profit.
        
        Args:
            ticket (int): Ticket number of position to modify
            stop_loss (float, optional): New stop loss price
            take_profit (float, optional): New take profit price
            
        Returns:
            bool: True if position modified successfully, False otherwise
        """
        if not self.is_connected():
            self.logger.error("Not connected to broker")
            return False
        
        self.logger.info(f"Modifying position with ticket: {ticket}")
        
        if self.platform == "MT5":
            return self._modify_position_mt5(ticket, stop_loss, take_profit)
        else:
            self.logger.error(f"Unsupported platform: {self.platform}")
            return False
    
    def get_positions(self) -> List[Dict[str, Any]]:
        """
        Get all open positions.
        
        Returns:
            List[Dict[str, Any]]: List of open positions with their details
        """
        if not self.is_connected():
            self.logger.error("Not connected to broker")
            return []
        
        if self.platform == "MT5":
            return self._get_positions_mt5()
        else:
            self.logger.error(f"Unsupported platform: {self.platform}")
            return []
    
    def get_account_info(self) -> Dict[str, Any]:
        """
        Get account information.
        
        Returns:
            Dict[str, Any]: Account information
        """
        if not self.is_connected():
            self.logger.error("Not connected to broker")
            return {}
        
        if self.platform == "MT5":
            return self._get_account_info_mt5()
        else:
            self.logger.error(f"Unsupported platform: {self.platform}")
            return {}
    
    # ===== MetaTrader 5 specific methods =====
    
    def _connect_mt5(self) -> bool:
        """
        Connect to MetaTrader 5 terminal.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        if not MT5_AVAILABLE:
            self.logger.error("MetaTrader5 package not installed")
            return False
        
        # Initialize MT5
        if not mt5.initialize(path=self.path, login=self.login, 
                             server=self.server, password=self.password):
            self.logger.error(f"MT5 initialization failed: {mt5.last_error()}")
            return False
        
        # Check connection
        if not mt5.terminal_info():
            self.logger.error("MT5 terminal info not available")
            mt5.shutdown()
            return False
        
        # Get account info
        account_info = mt5.account_info()
        if not account_info:
            self.logger.error(f"Failed to get account info: {mt5.last_error()}")
            mt5.shutdown()
            return False
        
        self.logger.info(f"Connected to MT5: {account_info.server}, Account: {account_info.login}")
        self._connected = True
        return True
    
    def _disconnect_mt5(self) -> bool:
        """
        Disconnect from MetaTrader 5 terminal.
        
        Returns:
            bool: True if disconnection successful, False otherwise
        """
        if not MT5_AVAILABLE:
            return False
        
        mt5.shutdown()
        self._connected = False
        self.logger.info("Disconnected from MT5")
        return True
    
    def _get_price_mt5(self, symbol: str) -> Optional[Dict[str, float]]:
        """
        Get current price for a symbol from MT5.
        
        Args:
            symbol (str): Symbol to get price for
            
        Returns:
            Optional[Dict[str, float]]: Dictionary with bid and ask prices, or None if error
        """
        # Get symbol info
        symbol_info = mt5.symbol_info(symbol)
        if not symbol_info:
            self.logger.error(f"Failed to get symbol info for {symbol}: {mt5.last_error()}")
            return None
        
        # Enable symbol if needed
        if not symbol_info.visible:
            if not mt5.symbol_select(symbol, True):
                self.logger.error(f"Failed to select symbol {symbol}: {mt5.last_error()}")
                return None
        
        # Get latest tick
        tick = mt5.symbol_info_tick(symbol)
        if not tick:
            self.logger.error(f"Failed to get tick for {symbol}: {mt5.last_error()}")
            return None
        
        return {
            "bid": tick.bid,
            "ask": tick.ask,
            "time": tick.time
        }
    
    def _place_market_order_mt5(
        self, 
        symbol: str, 
        order_type: OrderType, 
        lot_size: float, 
        stop_loss: float = None, 
        take_profit: float = None,
        comment: str = "Hunter Bot"
    ) -> Optional[int]:
        """
        Place a market order in MT5.
        
        Args:
            symbol (str): Symbol to trade
            order_type (OrderType): Order type (BUY or SELL)
            lot_size (float): Lot size
            stop_loss (float, optional): Stop loss price
            take_profit (float, optional): Take profit price
            comment (str, optional): Order comment
            
        Returns:
            Optional[int]: Order ticket number if successful, None if failed
        """
        # Get symbol info
        symbol_info = mt5.symbol_info(symbol)
        if not symbol_info:
            self.logger.error(f"Failed to get symbol info for {symbol}: {mt5.last_error()}")
            return None
        
        # Enable symbol if needed
        if not symbol_info.visible:
            if not mt5.symbol_select(symbol, True):
                self.logger.error(f"Failed to select symbol {symbol}: {mt5.last_error()}")
                return None
        
        # Convert OrderType to MT5 order type
        mt5_order_type = mt5.ORDER_TYPE_BUY if order_type == OrderType.BUY else mt5.ORDER_TYPE_SELL
        
        # Prepare request structure
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": float(lot_size),
            "type": mt5_order_type,
            "price": symbol_info.ask if order_type == OrderType.BUY else symbol_info.bid,
            "deviation": 10,  # Maximum price deviation in points
            "magic": 123456,  # Magic identifier
            "comment": comment,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        
        # Add SL/TP if provided
        if stop_loss is not None:
            request["sl"] = float(stop_loss)
        if take_profit is not None:
            request["tp"] = float(take_profit)
        
        # Send order
        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            self.logger.error(f"Order failed: {result.retcode}, {result.comment}")
            return None
        
        self.logger.info(f"Order executed: Ticket #{result.order}")
        return result.order
    
    def _close_position_mt5(self, ticket: int) -> bool:
        """
        Close a position in MT5 by ticket.
        
        Args:
            ticket (int): Ticket number of position to close
            
        Returns:
            bool: True if position closed successfully, False otherwise
        """
        # Get position info
        position = mt5.positions_get(ticket=ticket)
        if not position:
            self.logger.error(f"Position with ticket {ticket} not found: {mt5.last_error()}")
            return False
        
        # Position exists, prepare close request
        position = position[0]
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": position.symbol,
            "volume": position.volume,
            "type": mt5.ORDER_TYPE_BUY if position.type == 1 else mt5.ORDER_TYPE_SELL,  # Opposite of original order
            "position": position.ticket,
            "price": mt5.symbol_info_tick(position.symbol).ask if position.type == 1 else mt5.symbol_info_tick(position.symbol).bid,
            "deviation": 10,
            "magic": 123456,
            "comment": "Hunter Bot - Close Position",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        
        # Send order
        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            self.logger.error(f"Failed to close position: {result.retcode}, {result.comment}")
            return False
        
        self.logger.info(f"Position {ticket} closed successfully")
        return True
    
    def _modify_position_mt5(
        self, 
        ticket: int, 
        stop_loss: float = None, 
        take_profit: float = None
    ) -> bool:
        """
        Modify a position's stop loss and take profit in MT5.
        
        Args:
            ticket (int): Ticket number of position to modify
            stop_loss (float, optional): New stop loss price
            take_profit (float, optional): New take profit price
            
        Returns:
            bool: True if position modified successfully, False otherwise
        """
        # Get position info
        position = mt5.positions_get(ticket=ticket)
        if not position:
            self.logger.error(f"Position with ticket {ticket} not found: {mt5.last_error()}")
            return False
        
        # Prepare modify request
        position = position[0]
        request = {
            "action": mt5.TRADE_ACTION_MODIFY,
            "symbol": position.symbol,
            "position": position.ticket,
            "sl": float(stop_loss) if stop_loss is not None else position.sl,
            "tp": float(take_profit) if take_profit is not None else position.tp
        }
        
        # Send modify request
        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            self.logger.error(f"Failed to modify position: {result.retcode}, {result.comment}")
            return False
        
        self.logger.info(f"Position {ticket} modified successfully")
        return True
    
    def _get_positions_mt5(self) -> List[Dict[str, Any]]:
        """
        Get all open positions from MT5.
        
        Returns:
            List[Dict[str, Any]]: List of open positions with their details
        """
        positions = mt5.positions_get()
        if positions is None:
            error = mt5.last_error()
            if error[0] != 0:  # Error code 0 means no positions
                self.logger.error(f"Failed to get positions: {error}")
            return []