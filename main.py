import telebot
import validators
import requests

import os

import wget 

from time import strftime

from bs4 import BeautifulSoup
from fake_useragent import UserAgent


bot = telebot.TeleBot('1160872858:AAFO_2NxeC7w0v6Rq_m6B8K1wN5DA_4grw4')

def get_urls_from_url(url):

	try:
		response = requests.get(url)
	except:
		return False
	if response.status_code == 200 :

		parse = BeautifulSoup(response.text , 'html.parser')

		ret_urls = []

		for i in parse.findAll('a' , href = True):
			ret_urls.append( i['href'] )
		
		filename = strftime('%Y_%m_%d_%H_%M') + '.txt'

		parsed_data = open( filename , 'w')
		parsed_data.write('\n'.join(ret_urls))

		return filename

	return False

@bot.message_handler(commands=['start'])
def start_message(message):
	bot.send_message( message.from_user.id , 'Привет я бот , я умею разные приколюшки' )

@bot.message_handler(commands=['parse'])
def parse_message(  message ):
	url_to_parse = message.text.split(' ')[1]
	if validators.url( url_to_parse ):
		parsed_urls = get_urls_from_url( url_to_parse )
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


# @bot.message_handler(content_types=['text'])
# def url_message( message ):
# 	print( message.text )
# 	if validators.url( message.text ):
# 		parsed_urls = get_urls_from_url( message.text )
# 		print( parsed_urls )
# 		if parsed_urls:
# 			bot.send_message(message.chat.id ,'Почти готово .....')
# 			with open(parsed_urls , 'rb') as file:
# 				bot.send_document(message.chat.id , file)
# 			os.remove(parsed_urls)
# 		else:
# 			bot.send_message( message.chat.id , 'Не получилось, не фортануло' )
# 			bot.send_message( message.chat.id , 'Нет доступа к ресурсу , либо ресурс не существует' )
# 	else:
# 		bot.send_message( message.chat.id , 'Не валидный формат ссылки ....' )

bot.polling()
