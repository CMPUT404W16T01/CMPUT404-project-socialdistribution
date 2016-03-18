# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0003_auto_20160318_2058'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='author_id',
        ),
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.UUIDField(default='b74797fb-2f38-49c7-9445-170bff7c74ef'),
            preserve_default=False,
        ),
    ]
