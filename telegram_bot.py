#!/usr/bin/env python3
import ccxt
import asyncio
from telegram import Bot
from typing import Tuple

bot_token = 'add in token here'
chat_id = 'add in chat id here'

def check_pinbar(symbol: str, timeframe: str = '1h') -> Tuple[str, float, float, float, float]:
    exchange = ccxt.binance()
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe)

    open = [candle[1] for candle in ohlcv]
    high = [candle[2] for candle in ohlcv]
    low = [candle[3] for candle in ohlcv]
    close = [candle[4] for candle in ohlcv]

    bullish_pinbar = (close[-1] > open[-1] and
                      (high[-1] - max(open[-1], close[-1])) / (max(open[-1], close[-1]) - low[-1]) >= 2)

    bearish_pinbar = (close[-1] < open[-1] and
                      (low[-1] - min(open[-1], close[-1])) / (high[-1] - min(open[-1], close[-1])) >= 2)

    pinbar_type = "none"
    if bullish_pinbar:
        pinbar_type = "bullish"
    elif bearish_pinbar:
        pinbar_type = "bearish"

    return pinbar_type, close[-1], open[-1], high[-1], low[-1]

async def send_notification(bot_token: str, chat_id: str, message: str) -> None:
    bot = Bot(bot_token)
    await bot.send_message(chat_id=chat_id, text=message)

symbol = 'BTC/USDT'

pinbar_type, close, open, high, low = check_pinbar(symbol)

if pinbar_type != "none":
    asyncio.run(send_notification(bot_token, chat_id, f"Pinbar detected on the {symbol} 1-hour chart. Close: {close}, Open: {open}, High: {high}, Low: {low}"))
else:
    asyncio.run(send_notification(bot_token, chat_id, f"No Pinbar detected on the {symbol} 1-hour chart. Close: {close}, Open: {open}, High: {high}, Low: {low}"))


