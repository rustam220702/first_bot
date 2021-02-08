from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
from settings import TG_API_URL,TG_TOKEN
import logging
from glob import glob
from  random import choice
from bs4 import BeautifulSoup
from telegram import ReplyKeyboardRemove
from telegram.ext import ConversationHandler
import requests
from telegram import ReplyKeyboardMarkup,KeyboardButton
logging.basicConfig(format='%(asctime)s-%(levelname)s-%(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )

def sms(bot,update):
    print("Кто-то отправил мне комадну /start, что мне делать?")
    bot.message.reply_text("Здравствуйте, {}! \n"
                           "Меня создал Рустам".format(bot.message.chat.first_name),reply_markup=get_keyboard())

def parrot(bot,update):
    print(bot.message.text)
    bot.message.reply_text(bot.message.text)
def send_photo(bot, update):
    lists=glob('images/*')
    picture=choice(lists)
    update.bot.send_photo(chat_id=bot.message.chat.id,photo=open(picture,'rb'))
def get_contact(bot,update):
    print(bot.message.contact)
    bot.message.reply_text("{},мы получили ваш номер телефона".format(bot.message.chat.first_name))

def anketa_start(bot, update):
    bot.message.reply_text("Как вас зовут?",reply_markup=ReplyKeyboardRemove())
    return "user_name"
def anketa_get_name(bot, update):
    update.user_data['name']=bot.message.text
    print(bot.message.text)
    bot.message.reply_text("Напиши свой вариант, как улучшить бота")
    return "comment"
def anketa_get_comment(bot, update):
    update.user_data['comment']=bot.message.text
    print(bot.message.text)
    bot.message.reply_text("Спасибо за комментарий!",reply_markup=get_keyboard())
    return ConversationHandler.END
def get_anecdote(bot,update):
    receive=requests.get("http://anekdotme.ru/random")
    page=BeautifulSoup(receive.text,"html.parser")
    find=page.select(".anekdot_text")
    for text in find:
        page=(text.getText().strip())
    bot.message.reply_text(page)
def get_keyboard():
    contact_button=KeyboardButton("Отправить свои контакты",request_contact=True)
    my_keyboard = ReplyKeyboardMarkup([['Анекдот'],[contact_button],['Заполнить анкету'],['Фото']], resize_keyboard=True)
    return my_keyboard
def main():
    my_bot= Updater(TG_TOKEN, TG_API_URL, use_context=True)
    logging.info('Start bot')
    my_bot.start_polling()
    my_bot.dispatcher.add_handler(CommandHandler("start",sms))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Анекдот'),get_anecdote))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Начать'),sms))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Фото'), send_photo))
    my_bot.dispatcher.add_handler(ConversationHandler(entry_points=[MessageHandler(Filters.regex('Заполнить анкету'),anketa_start)],
                                                      states={
                                                        "user_name":[MessageHandler(Filters.text,anketa_get_name)],
                                                        "comment":[MessageHandler(Filters.text,anketa_get_comment)]
                                                      },
                                                      fallbacks=[]))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.contact, get_contact))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.text, parrot))
    my_bot.idle()

main()