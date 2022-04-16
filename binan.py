import config
from binance.client import Client
import pandas as pd

client = Client(config.bin_api_key, config.bin_secret_key)
klines = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")
print(klines)
