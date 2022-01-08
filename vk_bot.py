import os
from dotenv import load_dotenv
import random
import vk_api
from telegram_bot import detect_intent_texts
from vk_api.longpoll import VkLongPoll, VkEventType
from loger import logger

load_dotenv()


def send_message(event, vk_ap, text):
    vk_ap.messages.send(
        user_id=event.user_id,
        message=text,
        random_id=random.randint(1, 1000)
    )


def main():
    try:
        logger.info('start vkontakte bot')
        vk_token = os.getenv('VK_TOKEN')
        vk_session = vk_api.VkApi(token=vk_token)
        vk_ap = vk_session.get_api()
        longpoll = VkLongPoll(vk_session)
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                text = detect_intent_texts(event.text)
                if text != 'Я не понимаю о чём речь':
                    send_message(event, vk_ap, text)
    except Exception as ex:
        logger.warning(ex)



if __name__ == '__main__':
    main()
