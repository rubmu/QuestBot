# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-23 18:12
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_auto_20171223_1635'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='step',
            options={'ordering': ('number', 'title')},
        ),
        migrations.AlterField(
            model_name='condition',
            name='rule',
            field=models.CharField(choices=[('full_coincidence', 'Full coincidence'), ('to_be_in', 'To be in'), ('contains', 'Contains'), ('starts_with', 'Starts with'), ('ends_with', 'Ends with'), ('match_regex', 'Match regex'), ('contain_an_image', 'Contain an image'), ('contain_a_file', 'Contain a file'), ('contain_an_audio', 'Contain a audio'), ('contain_a_video', 'Contain a video'), ('received_before', 'Received before'), ('received_after', 'Received after')], default='full_coincidence', max_length=255, verbose_name='Pattern'),
        ),
        migrations.AlterField(
            model_name='event',
            name='send_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 23, 18, 12, 10, 936233, tzinfo=utc), verbose_name='Time to send on'),
        ),
    ]
