# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0006_auto_20160318_2252'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='is_markdown',
        ),
        migrations.RemoveField(
            model_name='post',
            name='is_markdown',
        ),
        migrations.AddField(
            model_name='comment',
            name='contentType',
            field=models.CharField(default=b' ', max_length=50),
        ),
        migrations.AddField(
            model_name='post',
            name='contentType',
            field=models.CharField(default=b' ', max_length=50),
        ),
    ]
