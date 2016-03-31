# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Img',
            fields=[
                ('primary_key', models.UUIDField(default=uuid.uuid4, serialize=False, primary_key=True)),
                ('image_blob', models.BinaryField()),
                ('parent', models.ForeignKey(to='feed.Post')),
            ],
        ),
    ]
