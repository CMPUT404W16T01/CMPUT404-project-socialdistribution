# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('display_name', models.CharField(max_length=60)),
                ('password', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=50)),
                ('bio', models.CharField(max_length=1000)),
                ('host', models.URLField(max_length=500)),
                ('github_account', models.CharField(max_length=30)),
                ('github_flag', models.BooleanField(default=False)),
                ('user_id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('comment_id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('body', models.CharField(max_length=1000)),
                ('is_markdown', models.BooleanField(default=False)),
                ('date_published', models.DateTimeField(auto_now=True)),
                ('author_id', models.ForeignKey(to='feed.Author')),
            ],
        ),
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('follower_id', models.UUIDField(serialize=False, primary_key=True)),
                ('followed_id', models.UUIDField()),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('post_id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('date_published', models.DateTimeField(auto_now=True)),
                ('body', models.CharField(max_length=1000)),
                ('is_markdown', models.BooleanField(default=False)),
                ('visibility', models.CharField(max_length=20)),
                ('image', models.ImageField(upload_to=b'')),
                ('author_id', models.ForeignKey(to='feed.Author')),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='post_id',
            field=models.ForeignKey(to='feed.Post'),
        ),
    ]
