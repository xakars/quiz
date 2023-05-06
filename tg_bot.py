from dotenv import load_dotenv
import os
import telegram
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters
from telegram import Update
from open_quiz import get_rand_quiz
import random
import redis


def start(update: Update, context: CallbackContext):
    custom_keyboard = [['Новый вопрос', 'Сдаться'],
                      ['Мой счёт']]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id,
                     text='Привет, я бот для викторин!',
                     reply_markup=reply_markup)


def handle_user_message(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    questions = get_rand_quiz()
    if update.message.text == 'Новый вопрос':
        question_answer_pairs = list(questions.items())
        question, answer = random.choice(question_answer_pairs)
        r.set(chat_id, question)
        context.bot.send_message(chat_id=update.effective_chat.id, text=question)
    elif update.message.text == questions.get(r.get(chat_id).decode()):
        context.bot.send_message(chat_id=update.effective_chat.id, text='Правильно! Поздравляю! Для следующего вопроса нажми «Новый вопрос»')
    elif update.message.text == 'Сдаться':
        pass
    elif update.message.text == 'Мой счёт':
        pass
    else:
        context.bot.send_message(chat_id=chat_id, text='Неправильный ответ, попробуйте еще раз')


if __name__ == '__main__':
    r = redis.Redis(host='localhost', port=6379, db=0)

    load_dotenv()
    token = os.environ['BOT_TOKEN']
    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(Filters.text & (~Filters.command), handle_user_message)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(echo_handler)
    updater.start_polling()
