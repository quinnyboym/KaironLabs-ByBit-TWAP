- Arbitrage logic contains major flaw, it should compare buying on exchange Bitvavo (ask price) and selling on exchange ByBit (bid price) or reverse, but not comparing both ask prices as these will only give you info about the buy prices.

- The while True loop calls the APIs non-stop, this risks rate limits. Using websockets for fast orderbook data would be much better, or at least add a time.sleep().

- The try/except blocks only print generic messages, making debugging harder. Capturing or logging more info on errors would help

- Multiple parameters (symbols, fees, order sizes) are hard-coded. This makes future extension more difficult, use .env instead and pass these through entire app

- Exchange is just a data container, not real OOP, a proper subclassing approach might be better, this is just passing some fields.

- Fee calculations uses the entire askVolume or bidVolume from the entire exchange rather than the actual "orderSize = min(...)" we are going to trade with

- The code only prints data rather than saving it in a log file or something like requested in the pdf

- Bybit & Binance uses testnet mode but Bitvavo does not. Consistency in test/production environments is very important, this bool should also be passed from main or in a .env var