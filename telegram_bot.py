import json
import os
import logging
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
from dotenv import load_dotenv
from google.cloud import dialogflow

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

def dialogflow_bot(update: Update, context: CallbackContext):
    text = detect_intent_texts(update.message.text)
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)

def detect_intent_texts(text):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""
    session_client = dialogflow.SessionsClient()
    path_json_config = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    with open(path_json_config, 'r') as f:
        config_json = json.load(f)
    project_id = config_json['project_id']
    session_id = config_json['client_id']
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=text, language_code='ru-RU')
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    return response.query_result.fulfillment_text


def main():
    token = os.getenv('TOKEN')
    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher
    dialogflow_bot_handler = MessageHandler(Filters.text & (~Filters.command), dialogflow_bot)
    dispatcher.add_handler(dialogflow_bot_handler)
    updater.start_polling()


if __name__ == '__main__':
    main()
