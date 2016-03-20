# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0010_git_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='friend',
            name='primary_key',
            field=models.UUIDField(default=uuid.uuid4, serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='friend',
            name='follower_id',
            field=models.UUIDField(),
        ),
    ]
