import os
import sys
import re
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

LOGGING = 1

def download_anime(url):
    driver.get(url)
    anime_name = driver.find_element(By.CLASS_NAME, 'shortstoryHead').text.split('/')[0].strip()
    if LOGGING: print(anime_name)
    try: os.mkdir(anime_name)
    except FileExistsError: pass

    episodes = driver.find_elements(By.CLASS_NAME, 'epizode')
    links = []
    for episode in episodes:
        ajax = episode.get_attribute('onclick')
        links.append(domain + re.search(r'(\d+),\d+', ajax).group(1) + '.mp4')
    name_format = r'{}\{:0{}}.mp4'
    name_len = len(str(len(episodes)))
    for i, link in enumerate(links, start=1):
        if LOGGING: print(f'\r{i}/{len(episodes)} episodes')
        file_name = name_format.format(anime_name, i, name_len)
        if (os.path.exists(file_name)) and (file_name in downloaded):
            continue
        else:
            download_file(link, file_name)
            with open('log.txt', 'a', encoding='utf-8') as log:
                log.write(file_name + '\n')

def download_file(url, file_path):
    with \
         open(file_path, 'wb') as f,\
         requests.get(url, stream=True) as r:
        for c in r.iter_content(chunk_size=4096):
            f.write(c)
    return True

def get_list_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as fin:
            return fin.read().splitlines()
    except FileNotFoundError:
        return []

domain = 'https://hd.trn.su/720/'
downloaded = get_list_from_file('log.txt')
urls = [url.replace('animevost.org', 'v2.vost.pw') for url in get_list_from_file('urls.txt')]

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors-spki-list')
options.add_argument('--ignore-ssl-errors')
options.add_argument('log-level=3')
with webdriver.Chrome(options=options) as driver:    
    for i, url in enumerate(urls, start=1):
        if LOGGING: print(f'{i}/{len(urls)} anime: ', end='')
        download_anime(url)
if LOGGING: print('All completed.')
