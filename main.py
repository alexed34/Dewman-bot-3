import os
import logging
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

def echo(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


def main(token):
    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)
    updater.start_polling()


if __name__ == '__main__':
    token = os.getenv('TOKEN')
    main(token)
