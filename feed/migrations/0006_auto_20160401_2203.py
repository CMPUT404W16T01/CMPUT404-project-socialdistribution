# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0005_auto_20160401_2012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='img',
            name='actual_image',
            field=models.ImageField(upload_to=b'images/'),
        ),
    ]
