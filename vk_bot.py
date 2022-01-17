import logging
import os
import random
import logging.config
import vk_api
from telegram import Bot
from dotenv import load_dotenv
from general_functions import TelegramLogsHandler, detect_intent_texts
from vk_api.longpoll import VkLongPoll, VkEventType


def send_message(event, vk_api_method, text):
    vk_api_method.messages.send(
        user_id=event.user_id,
        message=text,
        random_id=random.randint(1, 1000)
    )


def main():
    logging.config.fileConfig('logging.conf')
    logger = logging.getLogger("vkontakte_bot")

    hahdler_telegram = TelegramLogsHandler(Bot(token), chat_id)
    hahdler_telegram.setLevel(logging.WARNING)
    hahdler_telegram.setFormatter(logging.Formatter(f'%(asctime)s - %(filename)s- %(levelname)s - %(message)s'))

    logger.addHandler(hahdler_telegram)

    try:
        logger.info('start vkontakte bot')
        vk_session = vk_api.VkApi(token=vk_token)
        vk_api_method = vk_session.get_api()
        longpoll = VkLongPoll(vk_session)
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                text = detect_intent_texts(event.text, path_json_config)
                send_message(event, vk_api_method, text)
    except Exception as ex:
        logger.warning(ex)


if __name__ == '__main__':
    load_dotenv()
    vk_token = os.getenv('VK_TOKEN')
    token = os.getenv('TOKEN')
    chat_id = os.getenv('CHAT_ID')
    path_json_config = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    main()
