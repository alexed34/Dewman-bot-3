import logging
import os
from logging.handlers import RotatingFileHandler
from telegram import Bot
from dotenv import load_dotenv

load_dotenv()


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


logger = logging.getLogger("bot_loger")
logger.setLevel(logging.DEBUG)

handler_stream = logging.StreamHandler()
handler_stream.setLevel(logging.DEBUG)
handler_stream.setFormatter(logging.Formatter(f"%(asctime)s - %(process)d - %(levelname)s - %(message)s"))

handler_file = RotatingFileHandler("app.log", maxBytes=2000, backupCount=2)
handler_file.setLevel(logging.WARNING)
handler_file.setFormatter(logging.Formatter(f"%(asctime)s - %(process)d - %(levelname)s - %(message)s"))



chat_id = os.getenv('CHAT_ID')
token = os.getenv('TOKEN')
hahdler_telegram = TelegramLogsHandler(Bot(token), chat_id)
hahdler_telegram.setLevel(logging.WARNING)
hahdler_telegram.setFormatter(logging.Formatter(f"%(asctime)s - %(process)d - %(levelname)s - %(message)s"))


logger.addHandler(hahdler_telegram)
logger.addHandler(handler_file)
logger.addHandler(handler_stream)

