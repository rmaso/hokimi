# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import torneos.models.score_model
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('torneos', '0002_profile_email_confirmed'),
    ]

    operations = [
        migrations.CreateModel(
            name='Score',
            fields=[
                ('s_id', models.AutoField(serialize=False, primary_key=True)),
                ('submit_date', models.DateTimeField(auto_now_add=True)),
                ('description', models.CharField(max_length=255, blank=True)),
                ('document', models.FileField(upload_to=torneos.models.score_model.user_directory_path)),
                ('score', models.FloatField(blank=True)),
                ('error', models.CharField(max_length=255, blank=True)),
                ('competition', models.ForeignKey(to='torneos.Torneo')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
