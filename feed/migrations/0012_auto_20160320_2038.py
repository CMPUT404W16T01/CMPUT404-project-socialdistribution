# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('feed', '0011_auto_20160320_0144'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='author_id',
            new_name='author',
        ),
        migrations.AddField(
            model_name='foreignhost',
            name='foreign_username',
            field=models.ForeignKey(default='', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='foreignhost',
            name='url',
            field=models.CharField(max_length=500, serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='foreignhost',
            name='username',
            field=models.CharField(max_length=20),
        ),
    ]
