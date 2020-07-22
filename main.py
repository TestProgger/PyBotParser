import telebot
import validators
import os
from handlers import *

from telebot import types
bot = telebot.TeleBot('TOKEN')

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
	url_to_parse = message.text
	if validators.url( url_to_parse ):
		parsed_urls = get_urls_from_url(url_to_parse)
		if parsed_urls:
			bot.send_message(message.chat.id ,'Почти готово .....')
			with open(parsed_urls , 'rb') as file:
				bot.send_document(message.chat.id , file)
			os.remove(parsed_urls)
		else:
			bot.send_message( message.chat.id , 'Не получилось, не фортануло' )
			bot.send_message( message.chat.id , 'Нет доступа к ресурсу , либо ресурс не существует' )
	else:
		bot.send_message( message.chat.id , 'Не валидный формат ссылки ....' )

def parse_images(  message ):
	bot.send_message( message.chat.id, 'Придется подождать .....')
	url_to_parse = message.text
	if validators.url( url_to_parse ):
		parsed_images = get_images_from_url(url_to_parse ,message.chat.id )
		if parsed_images:
			bot.send_message(message.chat.id ,'Почти готово .....')
			with open(parsed_images , 'rb') as file:
				bot.send_document(message.chat.id , file)
			os.remove(parsed_images)
			
		else:
			bot.send_message( message.chat.id , 'Не получилось, не фортануло' )
			bot.send_message( message.chat.id , 'Нет доступа к ресурсу , либо ресурс не существует' )
	else:
		bot.send_message( message.chat.id , 'Не валидный формат ссылки ....' )


bot.polling()
