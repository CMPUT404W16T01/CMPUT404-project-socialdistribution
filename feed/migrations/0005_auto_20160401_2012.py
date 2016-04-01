# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0004_auto_20160331_1943'),
    ]

    operations = [
        migrations.RenameField(
            model_name='img',
            old_name='primary_key',
            new_name='id',
        ),
        migrations.AlterField(
            model_name='img',
            name='actual_image',
            field=models.ImageField(upload_to=b'images'),
        ),
    ]
