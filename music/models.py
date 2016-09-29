# -*- coding: utf8 -*-
from django.db import models


class Band(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='music/bands/bandImages/')

    def __str__(self):
        return self.name


    # def save(self, *args, **kwargs):
    #     if not self.pk:
    #         self.description = 'Some cool description'


class Album(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField('music/albums/albumImages/')
    band = models.ForeignKey(Band, on_delete=models.CASCADE)


class Song(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField()
    length = models.DurationField()
    song_file = models.FileField(upload_to='music/songs/songs/')
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    band = models.ForeignKey(Band, on_delete=models.CASCADE)