# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0014_auto_20160320_2057'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='git_post',
            name='id',
        ),
        migrations.AddField(
            model_name='git_post',
            name='primary_key',
            field=models.UUIDField(default=uuid.uuid4, serialize=False, primary_key=True),
        ),
    ]
