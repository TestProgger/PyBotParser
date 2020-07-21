import requests
import wget

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from time import strftime

import zipfile 
import os

def zip_dir(zipname, dir_to_zip):
    dir_to_zip_len = len(dir_to_zip.rstrip(os.sep)) + 1
    with zipfile.ZipFile(zipname, mode='w', compression=zipfile.ZIP_DEFLATED) as zf:
        for dirname, subdirs, files in os.walk(dir_to_zip):
            for filename in files:
                path = os.path.join(dirname, filename)
                entry = path[dir_to_zip_len:]
                zf.write(path, entry)

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
        return zipname

    return False
