# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0003_auto_20160331_1912'),
    ]

    operations = [
        migrations.RenameField(
            model_name='img',
            old_name='parent',
            new_name='parent_post',
        ),
        migrations.RemoveField(
            model_name='img',
            name='image_blob',
        ),
        migrations.AddField(
            model_name='img',
            name='actual_image',
            field=models.ImageField(default='', upload_to=b'images/whatever'),
            preserve_default=False,
        ),
    ]
