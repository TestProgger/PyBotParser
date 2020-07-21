import requests
import wget

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from time import strftime


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


def get_images_from_url(url):
    try:
        response = requests.get(url)
    except:
        return False
    if response.status_code == 200:

        parse = BeautifulSoup(response.text, 'html.parser')

        ret_urls = []

        for i in parse.findAll('img', src=True):
            ret_urls.append(i['src'])

        filename = strftime('images_%Y_%m_%d_%H_%M') + '.txt'

        parsed_data = open(filename, 'w')
        parsed_data.write('\n'.join(ret_urls))

        return filename

    return False
