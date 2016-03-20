# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0013_auto_20160320_2009'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentAuthor',
            fields=[
                ('comment_author_id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('id', models.UUIDField(editable=False)),
                ('host', models.URLField(max_length=500)),
                ('displayName', models.CharField(max_length=60)),
                ('url', models.CharField(max_length=500)),
                ('github', models.CharField(max_length=30)),
            ],
        ),
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(to='feed.CommentAuthor'),
        ),
    ]
