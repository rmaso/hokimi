# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import djangocms_text_ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bio', models.TextField(max_length=500, blank=True)),
                ('location', models.CharField(max_length=30, blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('signup_date', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='RegistrationQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question_type', models.CharField(max_length=2, choices=[(b'SC', b'Multiple Choice, Single Answer'), (b'MC', b'Multiple Choice, Multiple Answer'), (b'SA', b'Short Answer'), (b'AB', b'Agreement Check Box')])),
                ('question', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='RegistrationQuestionChoice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('choice', models.CharField(max_length=100)),
                ('question', models.ForeignKey(related_name='question_choice_set', to='torneos.RegistrationQuestion')),
            ],
        ),
        migrations.CreateModel(
            name='RegistrationQuestionResponse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text_response', models.TextField(blank=True)),
                ('agreed', models.BooleanField(default=False)),
                ('choices', models.ManyToManyField(related_name='response_set', to='torneos.RegistrationQuestionChoice', blank=True)),
                ('question', models.ForeignKey(related_name='response_set', to='torneos.RegistrationQuestion')),
                ('registration', models.ForeignKey(related_name='response_set', to='torneos.Registration')),
            ],
        ),
        migrations.CreateModel(
            name='Torneo',
            fields=[
                ('t_id', models.AutoField(serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('slug', models.SlugField()),
                ('short_description', models.CharField(max_length=200)),
                ('image', models.ImageField(upload_to=b'')),
                ('long_description', djangocms_text_ckeditor.fields.HTMLField()),
                ('end_date', models.DateTimeField(verbose_name=b'end date')),
                ('prizes', djangocms_text_ckeditor.fields.HTMLField(blank=True)),
                ('first_prize', models.CharField(max_length=50, blank=True)),
                ('evaluation', djangocms_text_ckeditor.fields.HTMLField()),
                ('data', djangocms_text_ckeditor.fields.HTMLField()),
                ('recruiting', models.BooleanField()),
                ('questions', models.ManyToManyField(to='torneos.RegistrationQuestion', blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='registration',
            name='competition',
            field=models.ForeignKey(to='torneos.Torneo'),
        ),
        migrations.AddField(
            model_name='registration',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
