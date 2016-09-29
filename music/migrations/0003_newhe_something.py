# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-29 09:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0002_auto_20160928_2005'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewHe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('song1', models.CharField(max_length=400)),
            ],
        ),
        migrations.CreateModel(
            name='Something',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('cname', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='')),
                ('length', models.DurationField()),
                ('song_file', models.FileField(upload_to='songs/')),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='music.Album')),
                ('band', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='music.Band')),
            ],
        ),
    ]
