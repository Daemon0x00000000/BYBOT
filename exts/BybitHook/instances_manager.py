import json
from exts.BybitHook._hook import BybitHook, WebSocket
from exts.TelegramHook.hook import TelegramHook
from dotenv import load_dotenv
import os


class InstancesManager:
    def __init__(self):
        load_dotenv()
        jsonConfig = json.load(open("config.json"))
        strategies = jsonConfig.keys()
        asset = os.getenv('ASSET')
        if asset is None:
            asset = 'SOLUSDT'
        tTOKEN = os.getenv('TELEGRAM_TOKEN')
        tCHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
        self.instances = {}
        tHook = TelegramHook(tTOKEN, tCHAT_ID)
        for strategy in strategies:
            self.instances[strategy] = BybitHook(jsonConfig[strategy]["API_KEY"], jsonConfig[strategy]["API_SECRET"],
                                                tHook,
                                                lambda: self.assetPrice, strategy, asset)

        self.ws = WebSocket(api_key='', api_secret='', retries=35, test=False)
        self.assetPrice = 0.0
        self.ws.instrument_info_stream(self.on_kline, symbol=asset)

    def on_kline(self, data):
        self.assetPrice = data['data']['last_price']

    def getInstance(self, strategy):
        return self.instances[strategy]
