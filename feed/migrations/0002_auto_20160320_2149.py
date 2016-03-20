# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0001_squashed_0015_auto_20160320_2139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foreignhost',
            name='foreign_username',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='friend',
            name='followed_host',
            field=models.URLField(max_length=500),
        ),
        migrations.AlterField(
            model_name='friend',
            name='follower_host',
            field=models.URLField(max_length=500),
        ),
    ]
