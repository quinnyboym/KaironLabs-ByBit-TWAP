import logging
import os
from exchange.bybit import Bybit
from strategy.TWAP import TWAP
from dotenv import load_dotenv

logging.basicConfig(
    filename="logs/twap.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
print("Started Kairon Labs TWAP Technical Assignment")

load_dotenv()

symbol = os.getenv("SYMBOL", "BTCUSDT")
side = os.getenv("SIDE", "Buy")
total_qty = float(os.getenv("TOTAL_QTY", "0.01"))
run_time = int(os.getenv("RUN_TIME", "300"))  # sec
freq = int(os.getenv("FREQ", "30"))  # sec
price_limit_str = os.getenv("PRICE_LIMIT", None)
price_limit = float(price_limit_str) if price_limit_str else None

exchange = Bybit(testnet=True)
strategy = TWAP(
    exchange=exchange,
    symbol=symbol,
    side=side,
    total_qty=total_qty,
    run_time=run_time,
    freq=freq,
    price_limit=price_limit
)

strategy.run()
logging.info("TWAP Finished - Made By Quinten Maes")
print("FINISHED, see logs/twap.log for more info")
