import json

from tqdm import tqdm


def generate_band():
    with open('no_duplicates.json') as f:
        data = json.load(f)

    text = open('lorem.txt').read()

    def get_schema():
        return {
            'name': '',
            'popularity': 0,
            'description': text,
            'image': '',
            'genres': []
        }

    records = []
    for artist in tqdm(data):
        schema = get_schema()
        schema['name'] = artist['name']
        schema['genre'] = artist['genres']
        schema['popularity'] = artist['popularity']
        try:
            schema['image'] = f'artists/{artist["id"]}.png'
        except:
            schema['image'] = ''
        records.append(schema)

    with open('bands_db.json', 'w') as f:
        json.dump(records, f)


def generate_albums():
    def generate_schema():
        return {
            'name': '',
            'image': '',
            'band': ''
        }

    with open('albums.json') as f:
        data = json.load(f)

    with open('no_duplicates.json') as f:
        bands = json.load(f)

    band_map = {x['id']: x['name'] for x in bands}

    records = []
    for album in tqdm(data):
        schema = generate_schema()
        schema['name'] = album['name']
        schema['image'] = f'albums/{album["id"]}.png'
        schema['band'] = band_map[album['artists']]
        records.append(schema)

    with open('albums_db.json', 'w') as f:
        json.dump(records, f)


generate_albums()