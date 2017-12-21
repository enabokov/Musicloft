from artist_list_parser import get_artists
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pprint import pprint
from tqdm import tqdm
import json
from contextlib import suppress

cred = SpotifyClientCredentials('f44728f72ed144c1a7a4adbd6f30b716', '28810db2ff0e49de9fa858fed89af4c3')
spotify = spotipy.Spotify(client_credentials_manager=cred)
artists = get_artists()


def get_artists_info(artists):
    results = []
    for artist in tqdm(artists):
        response = spotify.search(q='artist:' + artist, type='artist', limit=1)
        with suppress(Exception):
            results.append(response['artists']['items'][0])
    return results


def similar_to_artists(artists):
    results = []
    for artist in tqdm(artists):
        response = spotify.artist_related_artists(artist)
        with suppress(Exception):
            results.extend(response['artists'])
    return results


def artists_albums(artists):
    results = []
    for artist in tqdm(artists):
        response = spotify.artist_albums(artist)
        with suppress(Exception):
            for album in response['items']:
                album['artists'] = artist
                results.append(album)
    return results


with open('no_duplicates.json') as f:
    data = json.load(f)

ids = [x['id'] for x in data]

result = artists_albums(ids)

with open('albums.json', 'w') as f:
    json.dump(result, f)
