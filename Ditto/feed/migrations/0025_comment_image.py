# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0024_auto_20160309_2235'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='image',
            field=models.ImageField(default=datetime.datetime(2016, 3, 10, 2, 42, 3, 121638, tzinfo=utc), upload_to=b''),
            preserve_default=False,
        ),
    ]
