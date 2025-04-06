import logging
import unittest
from unittest.mock import MagicMock

from exchange.base_exchange import BaseExchange
from strategy.TWAP import TWAP


class TestTWAP(unittest.TestCase):

    def setUp(self):
        self.exchange = MagicMock(spec=BaseExchange)

        logging.getLogger().setLevel(logging.INFO)

    def test_price_limit_exceeded_buy(self):
        # Arrange
        symbol = "BTCUSDT"
        side = "buy"
        total_qty = 10
        run_time = 5
        freq = 1
        price_limit = 100

        # price limit reached
        self.exchange.get_market_price.return_value = 110.0

        # Act
        twap = TWAP(self.exchange, symbol, side, total_qty, run_time, freq, price_limit=price_limit)
        twap.run()

        # Assert
        # place_order was never called
        self.exchange.place_order.assert_not_called()

        with self.assertLogs(level='INFO') as captured_logs:
            twap.run()

        self.assertTrue(
            any("BONUS QUESTION: Price limit reached" in message for message in captured_logs.output),
            "'BONUS QUESTION: Price limit reached' message not found in logs."
        )

    def test_price_limit_exceeded_sell(self):
        # Arrange
        symbol = "BTCUSDT"
        side = "sell"
        total_qty = 10
        run_time = 5
        freq = 1
        price_limit = 100

        # price limit reached (for selling this is below price limit)
        self.exchange.get_market_price.return_value = 90.0

        # Act
        twap = TWAP(self.exchange, symbol, side, total_qty, run_time, freq, price_limit=price_limit)
        twap.run()

        # Assert
        # place_order was never called
        self.exchange.place_order.assert_not_called()

        with self.assertLogs(level='INFO') as captured_logs:
            twap.run()

        self.assertTrue(
            any("BONUS QUESTION: Price limit reached" in message for message in captured_logs.output),
            "'BONUS QUESTION: Price limit reached' message not found in logs."
        )

    def test_total_quantity_filled(self):
        # Arrange
        symbol = "BTCUSDT"
        side = "buy"
        total_qty = 10
        run_time = 10
        freq = 1

        twap = TWAP(self.exchange, symbol, side, total_qty, run_time, freq)

        self.exchange.get_market_price.return_value = 99.0

        self.exchange.place_order.return_value = {
            "result": {
                "orderId": "12345"
            }
        }

        def mock_get_order_details(symbol, order_id):
            # each run returns partial_fill of 2
            return {
                "result": {
                    "list": [{
                        "cumExecQty": 2.0
                    }]
                }
            }

        self.exchange.get_order_details.side_effect = mock_get_order_details

        # Act
        twap.run()

        # Assert
        with self.assertLogs(level='INFO') as captured_logs:
            twap.run()

        self.assertTrue(
            any("Total quantity filled" in message for message in captured_logs.output),
            "'Total quantity filled' message not found in logs."
        )