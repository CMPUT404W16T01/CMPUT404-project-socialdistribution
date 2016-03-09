# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0019_auto_20160308_1923'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='categories',
            field=models.CharField(default=b' ', max_length=1000),
        ),
        migrations.AddField(
            model_name='post',
            name='comment_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='post',
            name='contentType',
            field=models.CharField(default=b' ', max_length=100),
        ),
        migrations.AddField(
            model_name='post',
            name='description',
            field=models.CharField(default=b' ', max_length=150),
        ),
        migrations.AddField(
            model_name='post',
            name='origin',
            field=models.URLField(default=b' '),
        ),
        migrations.AddField(
            model_name='post',
            name='source',
            field=models.URLField(default=b' '),
        ),
        migrations.AddField(
            model_name='post',
            name='title',
            field=models.CharField(default=b' ', max_length=50),
        ),
    ]
