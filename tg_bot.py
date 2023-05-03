from dotenv import load_dotenv
import os
import telegram
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters
from telegram import Update


def start(update: Update, context: CallbackContext):
    custom_keyboard = [['Новый вопрос', 'Сдаться'],
                      ['Мой счёт']]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id,
                     text="Привет, я бот для викторин!",
                     reply_markup=reply_markup)


def handle_user_message(update: Update, context: CallbackContext):
    if update.message.text == 'Новый вопрос':
        context.bot.send_message(chat_id=update.effective_chat.id, text='message')
    if update.message.text == 'Сдаться':
        pass
    if update.message.text == 'Мой счёт':
        pass


if __name__ == '__main__':
    load_dotenv()
    token = os.environ["BOT_TOKEN"]
    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(Filters.text & (~Filters.command), handle_user_message)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(echo_handler)
    updater.start_polling()