import telebot
import validators
import os
from handlers import *

from telebot import types
bot = telebot.TeleBot('TOKEN')

bot_commands = [
				'/parse - вызов  парсера',
				'/image - обработчик изображения'
]

@bot.message_handler(commands=['start'])
def start_message(message):
	bot.send_message( message.from_user.id , 'Привет я бот , я умею разные приколюшки' )

	keyboard = types.InlineKeyboardMarkup()

	key_parse_url = types.InlineKeyboardButton(text = "Парсинг Ссылок Сайта" , callback_data='parse_url')
	keyboard.add( key_parse_url )

	key_parse_img = types.InlineKeyboardButton(text = "Парсинг Картинок Сайта" , callback_data='parse_img')
	keyboard.add( key_parse_img )

	bot.send_message(message.chat.id, text='Buttons', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker( call ):

	if call.data == 'parse_url':
		bot.send_message(call.message.chat.id , 'Дайте ссылку')
		bot.register_next_step_handler(call.message  , parse_urls)

	if call.data == 'parse_img':
		bot.send_message(call.message.chat.id , 'Дайте ссылку')
		bot.register_next_step_handler(call.message , parse_images)

	
def parse_urls(  message ):
	universal_parser(message , bot  , 'parse_urls')

def parse_images(  message ):
	universal_parser(message , bot , 'parse_images')


bot.polling()
