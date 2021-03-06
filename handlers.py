import requests

from bs4 import BeautifulSoup
from time import strftime

import zipfile 
import os
import shutil

import validators

# / 
#   @param zipname [ Название архива ]
#   @param dir_to_zip [ Название директории для архивации ]
#   @return None
# /
def zip_dir(zipname, dir_to_zip):
    dir_to_zip_len = len(dir_to_zip.rstrip(os.sep)) + 1
    with zipfile.ZipFile(zipname, mode='w', compression=zipfile.ZIP_DEFLATED) as zf:
        for dirname, subdirs, files in os.walk(dir_to_zip):
            for filename in files:
                path = os.path.join(dirname, filename)
                entry = path[dir_to_zip_len:]
                zf.write(path, entry)

# / 
#   @param url [ Валидная ссылка на сайт ]
#   @return filename [ Название файла со всеми ссылками которые удалось спарсить ]
# /
def get_urls_from_url(url):

    try:
        response = requests.get(url)
    except:
        return False
    if response.status_code == 200:

        parse = BeautifulSoup(response.text, 'html.parser')

        ret_urls = []

        for i in parse.findAll('a', href=True):
            ret_urls.append(i['href'])

        filename = strftime('urls_%Y_%m_%d_%H_%M') + '.txt'

        parsed_data = open(filename, 'w')
        parsed_data.write('\n'.join(ret_urls))

        return filename

    return False

# / 
#   @param url [ Валидная ссылка на сайт ]
#   @param chat_id [ id чата для которого парсятся картинки ]
#   @return zipname [ Название архива в котором сод-ся все картинки с сайта ]
# /
def get_images_from_url(url , chat_id):
    try:
        response = requests.get(url)
    except:
        return False
    if response.status_code == 200:

        parse = BeautifulSoup(response.text, 'html.parser')

        dirname = f'photos_{chat_id}'

        os.mkdir(dirname)
        for i in parse.findAll('img', src=True):
            try:
                response = requests.get(i['src'])
                open(f'{dirname}/{i["src"].split("/")[-1]}' , 'wb').write(response.content).close()
            except:
                pass
        
        zipname = strftime('images_%Y_%m_%d_%H_%M') + '.zip'

        zip_dir(zipname , dirname)
        shutil.rmtree(f'photos_{chat_id}')
        return zipname

    return False

#/
#   @param message [ Объект message содержащий все о сообщении и чате с пользоваателем ]
#   @param bot [ Объект класса Telebot ]
#   @param mode [ Режим на котором будет работать пасер { parse_url , parse_images } ]
#/
def universal_parser( message , bot  , mode ):
    url_to_parse = message.text
    if validators.url( url_to_parse ):
        bot.send_message( message.chat.id , 'Придется подождать ......' )  
        
        if mode == 'parse_urls':
            parsed_urls = get_urls_from_url(url_to_parse)
        else:
            parsed_urls = get_images_from_url(url_to_parse , message.chat.id)

        if parsed_urls:
            bot.send_message(message.chat.id ,'Почти готово .....')
            with open(parsed_urls , 'rb') as file:
                bot.send_document(message.chat.id , file)
            os.remove(parsed_urls)
        else:
        	bot.send_message( message.chat.id , 'Не получилось, не фортануло' )
    else:
        bot.send_message( message.chat.id , 'Не валидный формат ссылки ....' )