import random
import os
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from dotenv import load_dotenv
from vk_api.keyboard import VkKeyboard, VkKeyboardColor


def echo(event, vk_api, keyboard):
    vk_api.messages.send(
        user_id=event.user_id,
        message=event.text,
        random_id=random.randint(1,1000),
        keyboard=keyboard.get_keyboard()
    )


if __name__ == "__main__":
    load_dotenv()
    vk_token = os.environ["VK_TOKEN"]
    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()

    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Новый вопрос', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('Сдаться', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    keyboard.add_button('Мой счёт')


    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_api, keyboard)
