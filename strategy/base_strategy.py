from abc import ABC, abstractmethod

from exchange.base_exchange import BaseExchange


class BaseStrategy(ABC):
    def __init__(self, exchange: BaseExchange):
        self.exchange = exchange

    @abstractmethod
    def run(self):
        pass
