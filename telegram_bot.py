import logging
import logging.config
import os
from dotenv import load_dotenv
from telegram import Update, Bot
from telegram.ext import CallbackContext, Updater, MessageHandler, Filters

from detect_intent_texts import detect_intent_texts
from telegram_handler import TelegramLogsHandler


def send_message_telegram(update: Update, context: CallbackContext, ):
    path_json_config = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    response = detect_intent_texts(update.message.text, path_json_config)
    text = response.fulfillment_text
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def main():
    load_dotenv()
    token = os.getenv('TOKEN')
    chat_id = os.getenv('CHAT_ID')
    logging.config.fileConfig('logging.conf')
    logger = logging.getLogger("telegram_bot")

    hahdler_telegram = TelegramLogsHandler(Bot(token), chat_id)
    hahdler_telegram.setLevel(logging.WARNING)
    hahdler_telegram.setFormatter(logging.Formatter(f'%(asctime)s - %(filename)s- %(levelname)s - %(message)s'))

    logger.addHandler(hahdler_telegram)

    try:
        updater = Updater(token=token, use_context=True)
        dispatcher = updater.dispatcher
        dialogflow_bot_handler = MessageHandler(Filters.text & (~Filters.command), send_message_telegram)
        dispatcher.add_handler(dialogflow_bot_handler)
        updater.start_polling()
        logger.info('start telegram bot')
    except Exception as ex:
        logger.warning(ex)


if __name__ == '__main__':
    main()
