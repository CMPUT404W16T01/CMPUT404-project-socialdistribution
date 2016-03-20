# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='author',
            old_name='user_id',
            new_name='id',
        ),
        migrations.AddField(
            model_name='author',
            name='url',
            field=models.CharField(default=b' ', max_length=1000),
        ),
        migrations.AddField(
            model_name='comment',
            name='author_name',
            field=models.CharField(default=b' ', max_length=1000),
        ),
        migrations.AddField(
            model_name='post',
            name='author_name',
            field=models.CharField(default=b' ', max_length=1000),
        ),
    ]
