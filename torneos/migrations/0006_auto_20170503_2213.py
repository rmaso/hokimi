# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.files.storage


class Migration(migrations.Migration):

    dependencies = [
        ('torneos', '0005_auto_20170413_2329'),
    ]

    operations = [
        migrations.AddField(
            model_name='torneo',
            name='private_leaderboard_file',
            field=models.ImageField(default='', storage=django.core.files.storage.FileSystemStorage(base_url=b'/torneos/leaderboard', location=b'/Users/Ruben/Documents/heroku/hokimi'), upload_to=b'/private'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='torneo',
            name='public_leaderboard_file',
            field=models.ImageField(default='_', storage=django.core.files.storage.FileSystemStorage(base_url=b'/torneos/leaderboard', location=b'/Users/Ruben/Documents/heroku/hokimi'), upload_to=b'/public'),
            preserve_default=False,
        ),
    ]
