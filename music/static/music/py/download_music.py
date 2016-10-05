from __future__ import print_function

import os
import re

import pafy
import requests
from bs4 import BeautifulSoup


def extract_videos(html):
    soup = BeautifulSoup(html, 'html.parser')
    pattern = re.compile(r'/watch\?v=')
    found = soup.find_all('a', 'yt-uix-tile-link', href=pattern)
    return [(x.text.encode('utf-8'), x.get('href')) for x in found]


def make_request(url, hdr):
    http_proxy = os.environ.get("HTTP_PROXY")
    https_proxy = os.environ.get("HTTPS_PROXY")
    ftp_proxy = os.environ.get("FTP_PROXY")

    proxy_dict = {
        "http": http_proxy,
        "https": https_proxy,
        "ftp": ftp_proxy
    }

    req = requests.get(url, headers=hdr, proxies=proxy_dict)
    return req


def search_videos(query):
    response = make_request('https://www.youtube.com/results?search_query=' + query, {})
    return extract_videos(response.content)


def query_and_download(search):
    available = search_videos(search)
    title, video_link = available[0]
    title = title.decode('utf8')

    video = pafy.new('http://youtube.com/' + video_link)
    audiostreams = video.audiostreams
    formats = [(i, a.bitrate) for i, a in enumerate(audiostreams) if a.extension == 'm4a']
    index = max(formats, key=lambda item: item[1])[0]
    audiostreams[index].download()

    return title + '.m4a'


def download_song(name):
    search = name
    search = '+'.join(search.split())
    downloaded = query_and_download(search)
    return downloaded
