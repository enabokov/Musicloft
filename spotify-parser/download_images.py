import asyncio
import json
import os
from contextlib import suppress

import aiohttp
from tqdm import tqdm


async def fetch(session, url, name, folder):
    if os.path.exists(f'{folder}/{name}.png'):
        return

    async with session.get(url) as resp:
        data = await resp.read()

        with open(f'{folder}/{name}.png', 'wb') as f:
            f.write(data)


async def download_all_images(data):
    async with aiohttp.ClientSession() as sess:
        tasks = []
        for url, name, folder in tqdm(data, desc='Fill event loop with tasks'):
            future = fetch(sess, url, name, folder)
            tasks.append(future)

        await wait_for_all(tasks)


async def wait_for_all(tasks):
    sema = asyncio.Semaphore(20)
    waiter = tqdm(total=len(tasks))
    for task in tasks:
        async with sema:
            waiter.update(1)
            with suppress(Exception):
                await task


if __name__ == '__main__':
    with open('albums.json') as f:
        albums = json.load(f)

    with open('artists_similar.json') as f:
        artists = json.load(f)

    print(f'Albums: {len(albums)}')
    print(f'Artists: {len(artists)}')

    images_to_download = []

    for album in albums:
        with suppress(KeyError, IndexError):
            name = album['id']
            url = album['images'][0]['url']
            folder = 'albums'

            images_to_download.append((url, name, folder))

    for artist in artists:
        with suppress(KeyError, IndexError):
            name = artist['id']
            url = artist['images'][0]['url']
            folder = 'artists'

            images_to_download.append((url, name, folder))

    print(f'Total images: {len(images_to_download)}')

    asyncio.get_event_loop().run_until_complete(download_all_images(images_to_download))
