from urllib.request import urlopen

import spotipy
import wikipedia
from PyLyrics import *


def get_song_lyrics(artist, album, song):
    albums = PyLyrics.getAlbums(singer=artist)
    albums_names = [str(a).lower() for a in albums]
    try:
        album_obj = albums[albums_names.index(album.lower())]
    except:
        return ''
    songs = [str(a).lower() for a in album_obj.tracks()]
    try:
        return album_obj.tracks()[songs.index(song.lower())].getLyrics()
    except:
        return ''


def get_artist_info(name):
    results = sp.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        try:
            summary = wikipedia.summary(name, sentences=8)
        except wikipedia.exceptions.DisambiguationError as e:
            summary = ''
        artist = {
            'id': items[0]['id'],
            'name': items[0]['name'],
            'image': urlopen(items[0]['images'][0]['url']).read(),
            'popularity': items[0]['popularity'],
            'genres': items[0]['genres'],
            'description': summary
        }
        return artist
    else:
        return None


def artist_albums_songs(artist):
    albums = []
    results = sp.artist_albums(artist['id'], album_type='album')
    albums.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        albums.extend(results['items'])
    unique_albums = []
    for album in albums:
        if album['name'] not in [a['name'] for a in unique_albums]:
            temp = {
                'id': album['id'],
                'band': artist['name'],
                'name': album['name'],
                'image': urlopen(album['images'][0]['url']).read(),
                'songs': []
            }
            temp['songs'] = album_songs(temp['id'], artist['name'], album['name'])
            unique_albums.append(temp)
    return unique_albums


def album_songs(id, artist, album):
    tracks = []
    songs = []
    results = sp.album_tracks(id)
    tracks.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    for song in tracks:
        songs.append({
            'id': song['id'],
            'band': artist,
            'album': album,
            'name': song['name'],
            'duration': int(song['duration_ms'] / 100),
            'lyrics': get_song_lyrics(artist, album, song['name'])
        })
    return songs


sp = spotipy.Spotify()
sp.trace = False
