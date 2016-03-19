# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0007_auto_20160319_1748'),
    ]

    operations = [
        migrations.AddField(
            model_name='friend',
            name='followed_host',
            field=models.URLField(default='', max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='friend',
            name='follower_host',
            field=models.URLField(default='', max_length=500),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.CharField(default=b'', max_length=2000),
        ),
    ]
