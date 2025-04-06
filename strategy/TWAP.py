import time
import logging

from strategy.base_strategy import BaseStrategy
from exchange.base_exchange import BaseExchange


class TWAP(BaseStrategy):
    def __init__(self, exchange: BaseExchange, symbol, side, total_qty, run_time, freq, price_limit=None):
        super().__init__(exchange)
        self.symbol = symbol
        self.side = side
        self.total_qty = total_qty
        self.run_time = run_time
        self.freq = freq
        self.price_limit = price_limit

        self.num_iterations = int(run_time // freq)
        self.order_size = total_qty / self.num_iterations

    def run(self):
        logging.info(f"Starting TWAP for {self.symbol} side={self.side} total_qty={self.total_qty}")

        total_qty_filled = 0.0

        for i in range(1, self.num_iterations + 1):
            try:
                market_price = self.exchange.get_market_price(self.symbol, self.side)
                logging.info(f"[Run {i}] market_price = {market_price:.2f}")
                if self.price_limit is not None:
                    if (self.side.lower() == "buy" and market_price >= self.price_limit) or (self.side.lower() == "sell" and market_price <= self.price_limit):
                        logging.info(f"BONUS QUESTION: Price limit reached or exceeded at run # {i}. Exiting early.")
                        break

                resp = None
                for attempt in range(10):
                    try:
                        resp = self.exchange.place_order(
                            symbol=self.symbol,
                            side=self.side,
                            qty=self.order_size,
                            price=market_price
                        )
                        break
                    except Exception as e:
                        logging.warning(f"Order failed on attempt {attempt + 1}: {e}, retrying in 1s")
                        time.sleep(1)
                if not resp:
                    logging.error("place_order failed after 10 retries")
                    break

                oid = resp["result"]["orderId"]
                time.sleep(self.freq)

                details = self.exchange.get_order_details(self.symbol, oid)
                info = details["result"]["list"][0]
                partial_fill = float(info["cumExecQty"])
                total_qty_filled += partial_fill
                logging.info(f"Iteration {i} order {oid} filled={partial_fill}, total={total_qty_filled:.4f}")
                if total_qty_filled >= self.total_qty:
                    logging.info("Total quantity filled")
                    break

            except Exception as e:
                logging.error(f"Unexpected error on iteration {i}: {e}")
                break

        logging.info("Cancelling any remaining open orders")
        try:
            c = self.exchange.cancel_all_open_orders(self.symbol)
            logging.info(f"Cancel response: {c}")
        except Exception as e:
            logging.error(f"Failed to cancel remaining open orders: {e}")

        logging.info("TWAP completed")
