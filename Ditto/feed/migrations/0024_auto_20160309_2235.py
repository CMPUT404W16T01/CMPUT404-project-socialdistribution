# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0023_auto_20160309_2217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(default=datetime.datetime(2016, 3, 9, 22, 35, 15, 256317, tzinfo=utc), upload_to=b''),
            preserve_default=False,
        ),
    ]
