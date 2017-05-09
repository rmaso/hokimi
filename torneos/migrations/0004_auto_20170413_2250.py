# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('torneos', '0003_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='score',
            name='error',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='score',
            name='score',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
