import sys
import telegram
from telegram.error import TelegramError


class TelegramHook:
    def __init__(self, token, chat_id):
        self.bot = telegram.Bot(token=token)
        self.chat_id = chat_id

    async def __aenter__(self):
        await self.bot.initialize()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.bot.shutdown()

    async def sendMessage(self, message):
        try:
            await self.bot.send_message(chat_id=self.chat_id, text=message)
        except TelegramError as e:
            sys.stderr.write(f'TelegramError: {e}\n')

    async def sendPrefixedMessage(self, message, prefix):
        await self.sendMessage(f'{prefix} {message}')

    async def sendError(self, message):
        await self.sendPrefixedMessage(message, '\U0000274C [Error]')

    async def sendSuccess(self, message):
        await self.sendPrefixedMessage(message, '\U00002705 [Success]')

    async def sendInfo(self, message):
        await self.sendPrefixedMessage(message, '\U00002139 [Info]')
