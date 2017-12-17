import os

from django.contrib.auth.models import User
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


class Countries(models.Model):
    name = models.CharField(max_length=20)


class Genres(models.Model):
    name = models.CharField(max_length=255, unique=True)

    @classmethod
    def add_genre(cls, genre):
        try:
            cls.objects.create(
                name=genre,
            )
        except:
            pass
            # print(f'Genre {genre} was not added')


class Band(models.Model):
    name = models.CharField(max_length=100)
    popularity = models.IntegerField(default=0)
    image = models.ImageField(upload_to=update_filename)
    country = models.ForeignKey(Countries,
                                models.SET_NULL,
                                blank=True,
                                null=True)
    description = models.TextField()

    def __str__(self):
        return self.name

    def image_tag(self):
        return mark_safe('<img src="{}" width="150" height="150" />'.format(self.image.url))

    image_tag.short_description = 'Image'

    @classmethod
    def add_band(cls, band):

        # Add genres before insert band
        try:
            cls.objects.create(
                name=band['name'],
                popularity=band['popularity'],
                description=band['description'],
                image=band['image'],
            )
            for genre in band['genre']:
                BandGenres.add_genre(band['name'], genre)
        except Exception as e:
            print(f'Band {band["name"]} was not added {e}')


class BandGenres(models.Model):
    band = models.ForeignKey(Band, unique=False)
    genre = models.ForeignKey(Genres)

    @classmethod
    def add_genre(cls, band: str, genre: str):
        try:
            Genres.add_genre(genre)
        except:
            pass
        cls.objects.create(
            band=Band.objects.get(name=band),
            genre=Genres.objects.get(name=genre)
        )


class Album(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to=update_filename)
    band = models.ForeignKey(Band, on_delete=models.CASCADE)
    language = models.ForeignKey(Languages,
                                 models.SET_NULL,
                                 blank=True,
                                 null=True)
    budget = models.FloatField(blank=True, null=True)
    released_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name

    def image_tag(self):
        return mark_safe('<img src="{}" width="150" height="150" />'.format(self.image.url))

    image_tag.short_description = 'Image'

    @classmethod
    def add_album(cls, album, image_path):
        try:
            with open(image_path, 'rb') as f:
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
    genre = models.ForeignKey(Genres,
                              models.SET_NULL,
                              blank=True,
                              null=True)
    duration = models.IntegerField(blank=True, null=True)
    lyrics = models.TextField(default='No lyrics')
    song_file = models.FileField(upload_to=update_filename)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    band = models.ForeignKey(Band, on_delete=models.CASCADE)
    # img_url = models.ImageField(upload_to=update_filename)
    popularity = models.FloatField(blank=True, null=True)
    vote_average = models.FloatField(blank=True, null=True)
    vote_count = models.FloatField(blank=True, null=True)
    song_status = models.ForeignKey(Status,
                                    models.SET_NULL,
                                    blank=True,
                                    null=True)

    def __str__(self):
        return self.name

    @classmethod
    def add_song(cls, song, song_file):
        try:
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
        except:
            print(f'Song {song["name"]} was not added')

    def song_tag(self):
        return mark_safe('<audio controls><source src="{}"/></audio>'.format(self.song_file.url))

    song_tag.short_description = 'Song'


class LikedByUsers(models.Model):
    user = models.ForeignKey(User, unique=False)
    band = models.ForeignKey(Band, null=True)
