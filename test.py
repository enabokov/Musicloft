import json
from music.models import Band
from tqdm import tqdm

with open('bands_db.json') as f:
    data = json.load(f)


for band in tqdm(data):
    Band.add_band(band)