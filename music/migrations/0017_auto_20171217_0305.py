# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-17 03:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0016_auto_20171217_0036'),
    ]

    operations = [
        migrations.CreateModel(
            name='BandGenres',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('band', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='music.Band')),
            ],
        ),
        migrations.AlterField(
            model_name='genres',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AddField(
            model_name='bandgenres',
            name='genre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='music.Genres'),
        ),
    ]
