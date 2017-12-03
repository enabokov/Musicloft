import os

from django.core.files import File
from django.db import models
from django.utils.safestring import mark_safe


# Rename uploaded file with class attribute name
def update_filename(instance, filename):
    path = 'music/' + str.lower(instance.__class__.__name__) + '/'
    format = str(instance) + '.' + filename.split('.')[-1]

    path = os.path.join(path, format)
    return path if os.path.exists(path) else None


class Band(models.Model):
    name = models.CharField(max_length=100)
    popularity = models.IntegerField(default=0)
    description = models.TextField()
    image = models.ImageField(upload_to=update_filename)

    def __str__(self):
        return self.name

    def image_tag(self):
        return mark_safe('<img src="{}" width="150" height="150" />'.format(self.image.url))
    image_tag.short_description = 'Image'

    @classmethod
    def add_band(cls, artist):
        try:
            f = open('image.jpg', 'wb')
            f.write(artist['image'])
            f.close()
            f = File(open('image.jpg', 'rb'))

            cls.objects.create(name=artist['name'], popularity=artist['popularity'],
                               description=artist['description'], image=f)
            os.remove('image.jpg')
        except:
            pass


class Album(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to=update_filename)
    band = models.ForeignKey(Band, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def image_tag(self):
        return mark_safe('<img src="{}" width="150" height="150" />'.format(self.image.url))
    image_tag.short_description = 'Image'

    @classmethod
    def add_album(cls, album):
        try:
            f = open('image.jpg', 'wb')
            f.write(album['image'])
            f.close()
            f = File(open('image.jpg', 'rb'))

            cls.objects.create(name=album['name'], band=Band.objects.get(name=album['band']), image=f)
            os.remove('image.jpg')
        except:
            pass


class Song(models.Model):
    name = models.CharField(max_length=100)
    duration = models.IntegerField(blank=True, null=True)
    lyrics = models.TextField(default='')
    song_file = models.FileField(upload_to=update_filename)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    band = models.ForeignKey(Band, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    @classmethod
    def add_song(cls, song):
        try:
            song_file = download_song(song['band'] + ' - ' + song['name'])
            f = File(open(song_file, 'rb'))
            cls.objects.create(name=song['name'], duration=song['duration'], lyrics=song['lyrics'],
                               album=Album.objects.get(name=song['album']),
                               band=Band.objects.get(name=song['band']),
                               song_file=f)
            f.close()
            os.remove(song_file)
        except:
            pass

    def song_tag(self):
        return mark_safe('<audio controls><source src="{}"/></audio>'.format(self.song_file.url))
    song_tag.short_description = 'Song'
