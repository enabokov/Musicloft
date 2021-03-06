# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-16 22:58
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('music', '0013_auto_20171216_2255'),
    ]

    operations = [
        migrations.CreateModel(
            name='LikedByUsers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('band', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='music.Band')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='likedbyuser',
            name='band',
        ),
        migrations.RemoveField(
            model_name='likedbyuser',
            name='user',
        ),
        migrations.DeleteModel(
            name='LikedByUser',
        ),
    ]
