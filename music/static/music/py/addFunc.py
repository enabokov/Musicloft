from music.static.music.py.spotify import get_artist_info, artist_albums_songs
from music.views import Band, Song, Album

artists = ['atb', 'paul van dyk', 'schiller', 'avicii', 'kongos', 'imagine dragons', 'walk the moon', 'red hot chili peppers', 'System of a down', 'artic monkeys',
           'Sting', 'the offspring', 'Metallica', 'billy talent', 'pink floyd', 'the beatles',
           'led zeppelin', 'nirvana', 'the rolling stones', 'black sabbath', 'the who', 'radiohead', 'ac/dc',
           'iron maiden', "guns N'Roses", 'Ramones', 'green day', 'aerosmith', 'slipknot', 'van halen',
           'Judas priest', 'u2', 'twenty one pilots', 'Queen', 'deep purple', 'the clash', 'fleetwood mac',
           'the doors', 'the strokes', 'godsmack', 'slayer', 'evanescence', 'death', 'Talking heads', 'coldplay',
           'korn', 'rush', 'the beach boys', 'one direction', 'linkin park', 'my chemical romance', 'pearl jam',
           'Muse', 'the smiths', 'Megadeth']


def add_all(artists=artists):
    for artist in artists:
        try:
            artist_object = get_artist_info(artist)
            try:
                print(artist_object['name'], end=' - ')
                Band.add_band(artist_object)
                print('Success')

                for album in artist_albums_songs(artist_object):
                    print('\t' + album['name'], end=' - ')
                    try:
                        Album.add_album(album)
                        print('Success')

                        for song in album['songs']:
                            print('\t' + song['name'], end=' - ')
                            try:
                                Song.add_song(song)
                                print('Success')
                            except:
                                print('Failed')
                    except:
                        print('Failed')
            except:
                print('Failed')
        except:
            print('Failed')