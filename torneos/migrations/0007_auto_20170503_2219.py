# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.files.storage


class Migration(migrations.Migration):

    dependencies = [
        ('torneos', '0006_auto_20170503_2213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='torneo',
            name='private_leaderboard_file',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(base_url=b'/torneos/leaderboard', location=b'/Users/Ruben/Documents/heroku/hokimi'), upload_to=b'/private'),
        ),
        migrations.AlterField(
            model_name='torneo',
            name='public_leaderboard_file',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(base_url=b'/torneos/leaderboard', location=b'/Users/Ruben/Documents/heroku/hokimi'), upload_to=b'/public'),
        ),
    ]
