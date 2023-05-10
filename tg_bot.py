from dotenv import load_dotenv
import os
import telegram
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import Update
from open_quiz import get_rand_quiz, check_user_answer
import random
import redis
from enum import Enum


class State(Enum):
    QUESTION = 1
    ANSWER = 2


def start(update: Update, context: CallbackContext):
    custom_keyboard = [['Новый вопрос', 'Сдаться'], ['Мой счёт']]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id,
                     text='Привет, Я бот для викторин',
                     reply_markup=reply_markup)

    return State.QUESTION


def handle_new_question_request(update, context):
    chat_id = update.effective_chat.id
    questions = get_rand_quiz()
    question_answer_pairs = list(questions.items())
    question, answer = random.choice(question_answer_pairs)
    r.set(chat_id, answer)
    context.bot.send_message(chat_id=update.effective_chat.id, text=question)

    return State.ANSWER


def handle_solution_attempt(update, context):
    chat_id = update.effective_chat.id
    correct_answer = r.get(chat_id).decode()
    message_text = update.message.text

    if check_user_answer(correct_answer, message_text):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Правильно! Поздравляю! Для следующего вопроса нажми «Новый вопрос»')
        return State.QUESTION
    else:
        context.bot.send_message(chat_id=chat_id, text='Неправильный ответ, попробуйте еще раз')


def handle_give_up(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    correct_answer = r.get(chat_id).decode()
    context.bot.send_message(chat_id=chat_id, text=f"Правильный ответ: {correct_answer}")
    context.bot.send_message(chat_id=chat_id, text="Хорошо, попробуем следующий вопрос. Нажмите «Новый вопрос»")
    return State.QUESTION


if __name__ == '__main__':
    r = redis.Redis(host='localhost', port=6379, db=0)

    load_dotenv()
    token = os.environ['BOT_TOKEN']
    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher

    conv_handler=ConversationHandler(
            entry_points=[
                CommandHandler('start', start),
            ],

            states={
                State.QUESTION: [MessageHandler(Filters.regex('^Новый вопрос$'), handle_new_question_request)],
                State.ANSWER:  [
                    MessageHandler(Filters.regex('^Сдаться$'), handle_give_up),
                    MessageHandler(Filters.text, handle_solution_attempt),
                ],
            },

            fallbacks=[]
    )

    dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()
