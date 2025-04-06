from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseExchange(ABC):
    @abstractmethod
    def get_market_price(self, symbol: str, side: str) -> float:
        pass

    @abstractmethod
    def place_order(self, symbol: str, side: str, qty: float, price: float = None) -> Any:
        pass

    @abstractmethod
    def cancel_all_open_orders(self, symbol: str) -> Any:
        pass

    @abstractmethod
    def get_order_details(self, symbol: str, order_id: str) -> Any:
        pass
