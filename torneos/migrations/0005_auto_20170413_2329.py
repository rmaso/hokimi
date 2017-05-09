# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('torneos', '0004_auto_20170413_2250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='score',
            name='competition',
            field=models.ForeignKey(blank=True, to='torneos.Torneo', null=True),
        ),
        migrations.AlterField(
            model_name='score',
            name='user',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
