import os
from vk_api.longpoll import VkLongPoll, VkEventType
from dotenv import load_dotenv
import random
import vk_api as vk
from telegram_bot import detect_intent_texts

load_dotenv()


def send_message(event, vk_api, text):
    vk_api.messages.send(
        user_id=event.user_id,
        message=text,
        random_id=random.randint(1, 1000)
    )


def main():
    vk_token = os.getenv('VK_TOKEN')
    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            text = detect_intent_texts(event.text)
            if text != 'Я не понимаю о чём речь':
                send_message(event, vk_api, text)


if __name__ == '__main__':
    main()
