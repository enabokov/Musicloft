# -*- coding: utf8 -*-
import os

from django.db import models


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


class Album(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to=update_filename)
    band = models.ForeignKey(Band, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Song(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField()
    length = models.DurationField()
    song_file = models.FileField(upload_to=update_filename)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    band = models.ForeignKey(Band, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
