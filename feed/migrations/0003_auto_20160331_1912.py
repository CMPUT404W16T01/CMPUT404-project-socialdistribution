# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0002_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='img',
            name='image_blob',
            field=models.ImageField(upload_to=b''),
        ),
    ]
