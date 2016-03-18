# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0004_auto_20160318_2239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.UUIDField(default=uuid.uuid4),
        ),
    ]
