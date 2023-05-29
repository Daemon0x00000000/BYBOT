import sys
from pybit.usdt_perpetual import HTTP, WebSocket
import asyncio
from pybit.exceptions import FailedRequestError, InvalidRequestError
import time


class BybitHook:
    def __init__(self, key, secret, telegramCallback, priceCallback, name, asset):
        api_key = key
        api_secret = secret
        if api_key is None or api_secret is None:
            raise Exception("API_KEY or API_SECRET is not set")
        retries = 0
        while True:
            try:
                retries += 1
                self.ws = WebSocket(api_key=api_key, api_secret=api_secret, retries=35, test=False)
                self.client = HTTP(api_key=api_key, api_secret=api_secret, force_retry=True, max_retries=35)
                break
            except Exception as e:
                if retries > 5:
                    sys.exit(f"Unable to connect to Bybit API : {e}")
                else:
                    print(f"Unable to connect to Bybit API : {e}")
                    continue
        self.ws.position_stream(self.on_order)
        self.ws.wallet_stream(self.on_wallet)

        self.currentPosition: str = ''
        self.available_balance = self.get_balance()
        self.getPrice = priceCallback
        self.tHook = telegramCallback
        self.name = name
        self.asset = asset

    def on_order(self, data):
        currentPosition = f'{data["data"][0]["user_id"]}-{data["data"][0]["position_id"]}'
        qty = data['data'][0]['size']
        if currentPosition == self.currentPosition and float(qty) == 0.0:
            self.currentPosition = ''
        else:
            self.currentPosition = currentPosition

    def on_wallet(self, data):
        if self.currentPosition == '':
            self.available_balance = data['data'][0]['available_balance']

    def get_balance(self):
        try:
            result = self.client.get_wallet_balance()
            return result['result']['USDT']['available_balance']
        except (FailedRequestError, InvalidRequestError) as e:
            asyncio.run(self.sendMessage(f"Unable to get balance : {e.message}", 'error'))
            return None

    def place_order(self, side) -> None:
        retries = 0
        asset = self.asset
        while retries <= 3:
            try:
                balance = self.available_balance
                if balance is None:
                    return
                solusdtperp = self.getPrice()
                if solusdtperp is None:
                    return
                qty = str(float(balance * 0.99) / float(solusdtperp))[:7]

                asyncio.run(self.sendMessage(f'Atempting to place order : {side} {qty} {asset}', 'info'))
                self.client.place_active_order(symbol=asset, qty=qty, side=side, order_type="Market",
                                               time_in_force="GoodTillCancel", reduce_only=False,
                                               close_on_trigger=False)
                timestamp = time.time()
                while self.currentPosition == '':
                    if time.time() - timestamp > 5:
                        break
                    pass
                asyncio.run(self.sendMessage(f'Order placed : {side} {qty} {asset}', 'success'))
                break
            except (FailedRequestError, InvalidRequestError) as e:
                retries += 1
                asyncio.run(self.sendMessage(f"Attempt {retries} : Unable to place order : {e.message}", 'error'))
                if retries >= 3:
                    asyncio.run(self.sendMessage(f"Unable to place order : {e.message}", 'error'))

    def close_order(self):
        try:
            self.client.close_position(self.asset)
            # self.client.cancel_all_active_orders(symbol=symbol)
            asyncio.run(self.sendMessage(f'Atempting to close order : {self.asset}', 'info'))
            timestamp = time.time()
            while self.currentPosition != '':
                if time.time() - timestamp > 5:
                    break
                pass
            asyncio.run(self.sendMessage(f'Order closed : {self.asset}', 'success'))
        except Exception as e:
            asyncio.run(self.sendMessage(f"Unable to close order : {e}", 'error'))
            return None

    async def sendMessage(self, message, status):
        message = f'{self.name} : {message}'
        if status == 'info':
            await self.tHook.sendInfo(message)
        elif status == 'success':
            await self.tHook.sendSuccess(message)
        elif status == 'error':
            await self.tHook.sendError(message)
