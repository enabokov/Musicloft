import os
from contextlib import suppress

from bs4 import BeautifulSoup


def get_artists():
    FOLDER = 'htmls'
    artists = []
    for file in os.listdir(FOLDER):
        if not file.endswith('.html'):
            continue
        with open(f'{FOLDER}/{file}', encoding='utf-8') as f:
            data = f.read()

        soup = BeautifulSoup(data, "html.parser")
        tags = soup.findAll('a')
        for tag in tags:
            with suppress(Exception):
                if 'listItem__title--link' in tag['class']:
                    artists.append(tag.text)
    return set(artists)
