import logging
import os

from dotenv import load_dotenv

load_dotenv()

chat_id = os.getenv('CHAT_ID')
token = os.getenv('TOKEN')


class TelegramLogsHandler(logging.Handler):
    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


logger_config = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {'std_format': {'format': f"%(asctime)s - %(process)d - %(levelname)s - %(message)s"}},
    'handlers': {'console': {'class': 'logging.StreamHandler',
                             'level': 'DEBUG',
                             'formatter': 'std_format'
                             },
                 'file': {'class': 'logging.handlers.RotatingFileHandler',
                          'level': 'DEBUG',
                          'formatter': 'std_format',
                          'filename': 'app.log',
                          'maxBytes': 2000,
                          'backupCount': 2,
                          },
                 'telegram': {'class': 'handlers.TelegramLogsHandler',
                              'level': 'DEBUG',
                              'formatter': 'std_format',
                              # 'chat_id': '<chat_id>',
                              # 'tg_bot': '<tg_bot>',

                              }
                 },
    'loggers': {'bot_loger': {
        'level': 'DEBUG',
        'handlers': ['console', 'file', 'telegram']

    }},
}
