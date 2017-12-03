import os

from django.core.files import File
from django.db import models
from django.utils.safestring import mark_safe


# Rename uploaded file with class attribute name
# from _download_script import download_song


def update_filename(instance, filename):
    path = 'music/' + str.lower(instance.__class__.__name__) + '/'
    format = str(instance) + '.' + filename.split('.')[-1]

    path = os.path.join(path, format)
    return path if os.path.exists(path) else None


class Languages(models.Model):
    name = models.CharField(max_length=15)


class Status(models.Model):
    name = models.CharField(max_length=15)


class Genres(models.Model):
    name = models.CharField(max_length=10)


class Countries(models.Model):
    name = models.CharField(max_length=20)


class Band(models.Model):
    name = models.CharField(max_length=100)
    popularity = models.IntegerField(default=0)
    image = models.ImageField(upload_to=update_filename)
    country = models.ForeignKey(Countries, default='Unknown country')
    description = models.TextField()

    def __str__(self):
        return self.name

    def image_tag(self):
        return mark_safe('<img src="{}" width="150" height="150" />'.format(self.image.url))

    image_tag.short_description = 'Image'

    @classmethod
    def add_band(cls, artist):
        try:
            with open('image.jpg', 'wb') as f:
                f.write(artist['image'])

            with open('image.jpg', 'rb') as f:
                cls.objects.create(
                    name=artist['name'],
                    popularity=artist['popularity'],
                    description=artist['description'],
                    image=File(f),
                    country=artist['country'],
                )

            os.remove('image.jpg')
        except:
            print(f'Band {artist["name"]} was not added')


class Album(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to=update_filename)
    band = models.ForeignKey(Band, on_delete=models.CASCADE)
    language = models.ForeignKey(Languages, default='Unknown language')
    budget = models.FloatField(blank=True, null=True)
    released_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name

    def image_tag(self):
        return mark_safe('<img src="{}" width="150" height="150" />'.format(self.image.url))

    image_tag.short_description = 'Image'

    @classmethod
    def add_album(cls, album):
        try:
            with open('image.jpg', 'wb') as f:
                f.write(album['image'])

            with open('image.jpg', 'rb') as f:
                cls.objects.create(
                    name=album['name'],
                    image=File(f),
                    band=Band.objects.get(name=album['band']),
                    languages=Languages.objects.get(name=album['language']),
                    budget=album['budget'],
                    released_date=album['released_date'],
                )

            os.remove('image.jpg')
        except:
            print(f'Album {album["name"]} was not added')


class Song(models.Model):
    name = models.CharField(max_length=100)
    genre = models.ForeignKey(Genres, default='Unknown genre')
    duration = models.IntegerField(blank=True, null=True)
    lyrics = models.TextField(default='No lyrics')
    song_file = models.FileField(upload_to=update_filename)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    band = models.ForeignKey(Band, on_delete=models.CASCADE)
    # img_url = models.ImageField(upload_to=update_filename)
    popularity = models.FloatField(blank=True, null=True)
    vote_average = models.FloatField(blank=True, null=True)
    vote_count = models.FloatField(blank=True, null=True)
    song_status = models.ForeignKey(Status, default='Unknown status')

    def __str__(self):
        return self.name

    @classmethod
    def add_song(cls, song):
        try:
            song_file = download_song(song['band'] + ' - ' + song['name'])

            with open(song_file, 'rb') as f:
                cls.objects.create(
                    name=song['name'],
                    genre=Genres.objects.get(name=song['genre']),  # new field
                    duration=song['duration'],
                    lyrics=song['lyrics'],
                    song_file=File(f),
                    album=Album.objects.get(name=song['album']),
                    band=Band.objects.get(name=song['band']),
                    img_url=song['img_url'],  # new field
                    popularity=song['popularity'],  # new field
                    vote_average=song['vote_average'],  # new field
                    vote_count=song['vote_count'],  # new field
                    song_status=song['song_status'],  # new field
                )

            os.remove(song_file)
        except:
            print(f'Song {song["name"]} was not added')

    def song_tag(self):
        return mark_safe('<audio controls><source src="{}"/></audio>'.format(self.song_file.url))

    song_tag.short_description = 'Song'
