import os
from typing import Any
from pybit.unified_trading import HTTP

from exchange.base_exchange import BaseExchange


class Bybit(BaseExchange):
    def __init__(self, testnet: bool = True):
        self.session = HTTP(
            testnet=testnet,
            api_key=os.getenv("BYBIT_API_KEY"),
            api_secret=os.getenv("BYBIT_API_SECRET"),
        )

    def place_order(self, symbol: str, side: str, qty: float, price: float = None) -> Any:
        if price is not None:
            # limit
            return self.session.place_order(
                category="spot",
                symbol=symbol,
                side=side,
                orderType="Limit",
                qty=qty,
                price=str(round(price, 2)),
                timeInForce="IOC",   # Immediate or Cancel
            )
        else:
            # market
            return self.session.place_order(
                category="spot",
                symbol=symbol,
                side=side,
                orderType="Market",
                qty=qty,
                marketUnit="baseCoin"  # for BTCUSDT this means qty will be BTC qty
            )

    def get_market_price(self, symbol: str, side: str) -> float:
        tickers = self.session.get_tickers(category="spot", symbol=symbol)

        data_list = tickers["result"]["list"]
        if not data_list:
            raise ValueError(f"ERROR no ticker data for {symbol}")

        info = data_list[0]
        bid1 = float(info["bid1Price"])
        ask1 = float(info["ask1Price"])
        if side.lower() == "buy":
            return ask1
        else:
            return bid1

    def cancel_all_open_orders(self, symbol: str) -> Any:
        return self.session.cancel_all_orders(category="spot", symbol=symbol)

    def get_order_details(self, symbol: str, order_id: str) -> Any:
        return self.session.get_open_orders(category="spot", symbol=symbol, orderId=order_id)
