import random
import os
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from dotenv import load_dotenv
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from open_quiz import get_rand_quiz, check_user_answer
import redis
import argparse


def replay(event, vk_api, keyboard, message):
    vk_api.messages.send(
        user_id=event.user_id,
        message=message,
        random_id=random.randint(1,1000),
        keyboard=keyboard.get_keyboard()
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', default='quiz-questions', help='path to quizzes files')
    args = parser.parse_args()
    path_to_quizzes = args.path
    quizzes_file_names = os.listdir(path_to_quizzes)
    path_to_rand_quiz_file = os.path.join(path_to_quizzes, random.choice(quizzes_file_names))

    r = redis.Redis(host='localhost', port=6379, db=0)

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
            if event.text == 'Новый вопрос':
                questions = get_rand_quiz(path_to_rand_quiz_file)
                question_answer_pairs = list(questions.items())
                question, answer = random.choice(question_answer_pairs)
                r.set(event.user_id, answer)
                message = question
                replay(event, vk_api, keyboard, message)
            elif event.text == 'Сдаться':
                correct_answer = r.get(event.user_id).decode()
                message = f"Правильный ответ: {correct_answer}"
                replay(event, vk_api, keyboard, message)
            elif check_user_answer(r.get(event.user_id).decode(), event.text):
                message='Правильно! Поздравляю! Для следующего вопроса нажми «Новый вопрос»'
                replay(event, vk_api, keyboard, message)
            else:
                message = 'Неправильный ответ, попробуйте еще раз'
                replay(event, vk_api, keyboard, message)
