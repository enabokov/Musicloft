import os

from django.db import models
from django.utils.safestring import mark_safe


# Rename uploaded file with class attribute name
def update_filename(instance, filename):
    path = 'music/' + str.lower(instance.__class__.__name__) + '/'
    format = str(instance) + '.' + filename.split('.')[-1]
    return os.path.join(path, format)


class Band(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to=update_filename)

    def __str__(self):
        return self.name

    def image_tag(self):
        return mark_safe('<img src="{}" width="150" height="150" />'.format(self.image.url))

    image_tag.short_description = 'Image'


class Album(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to=update_filename)
    band = models.ForeignKey(Band, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def image_tag(self):
        return mark_safe('<img src="{}" width="150" height="150" />'.format(self.image.url))

    image_tag.short_description = 'Image'


class Song(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)
    song_file = models.FileField(upload_to=update_filename)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    band = models.ForeignKey(Band, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def image_tag(self):
        return mark_safe('<img src="{}" width="150" height="150" />'.format(self.image.url))

    image_tag.short_description = 'Image'

    def song_tag(self):
        return mark_safe('<audio controls><source src="{}"/></audio>'.format(self.song_file.url))

    song_tag.short_description = 'Song'

        # TODO add calculate duration function
