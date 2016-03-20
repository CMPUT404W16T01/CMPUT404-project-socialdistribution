# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import uuid


class Migration(migrations.Migration):

    replaces = [(b'feed', '0001_initial'), (b'feed', '0002_auto_20160317_2155'), (b'feed', '0003_auto_20160318_2058'), (b'feed', '0004_auto_20160318_2239'), (b'feed', '0005_auto_20160318_2242'), (b'feed', '0006_auto_20160318_2252'), (b'feed', '0007_auto_20160319_1748'), (b'feed', '0008_auto_20160319_1826'), (b'feed', '0009_foreignhost'), (b'feed', '0010_git_post'), (b'feed', '0011_auto_20160320_0144'), (b'feed', '0012_auto_20160320_1930'), (b'feed', '0013_auto_20160320_2009'), (b'feed', '0014_auto_20160320_2057'), (b'feed', '0015_auto_20160320_2139')]

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('user_id', models.UUIDField(serialize=False, editable=False, primary_key=True)),
                ('display_name', models.CharField(max_length=60)),
                ('bio', models.CharField(default=b' ', max_length=1000)),
                ('host', models.URLField(max_length=500)),
                ('github_account', models.CharField(default=b' ', max_length=30)),
                ('github_flag', models.BooleanField(default=False)),
                ('admin_auth', models.BooleanField(default=False)),
                ('email', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('comment_id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('body', models.CharField(max_length=1000)),
                ('is_markdown', models.BooleanField(default=False)),
                ('date_published', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(upload_to=b'', blank=True)),
                ('author_id', models.ForeignKey(to='feed.Author')),
            ],
        ),
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('follower_id', models.UUIDField()),
                ('followed_id', models.UUIDField()),
                ('followed_host', models.URLField(default='', max_length=500)),
                ('follower_host', models.URLField(default='', max_length=500)),
                ('primary_key', models.UUIDField(default=uuid.uuid4, serialize=False, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('content', models.CharField(max_length=1000)),
                ('visibility', models.CharField(max_length=20)),
                ('image', models.ImageField(upload_to=b'', blank=True)),
                ('title', models.CharField(default=b' ', max_length=50)),
                ('source', models.URLField(default=b' ')),
                ('origin', models.URLField(default=b' ')),
                ('description', models.CharField(default=b' ', max_length=150)),
                ('count', models.IntegerField(default=0)),
                ('categories', models.CharField(default=b' ', max_length=1000)),
                ('author', models.ForeignKey(to='feed.Author')),
                ('published', models.DateTimeField(default=django.utils.timezone.now)),
                ('contentType', models.CharField(default=b' ', max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='post_id',
            field=models.ForeignKey(to='feed.Post'),
        ),
        migrations.RenameField(
            model_name='author',
            old_name='user_id',
            new_name='id',
        ),
        migrations.AddField(
            model_name='author',
            name='url',
            field=models.CharField(default=b' ', max_length=500),
        ),
        migrations.AddField(
            model_name='comment',
            name='author_name',
            field=models.CharField(default=b' ', max_length=1000),
        ),
        migrations.RenameField(
            model_name='author',
            old_name='display_name',
            new_name='displayName',
        ),
        migrations.RenameField(
            model_name='author',
            old_name='github_account',
            new_name='github',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='body',
            new_name='comment',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='comment_id',
            new_name='id',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='date_published',
        ),
        migrations.AddField(
            model_name='comment',
            name='published',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.RemoveField(
            model_name='comment',
            name='author_id',
        ),
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(to='feed.CommentAuthor'),
        ),
        migrations.RemoveField(
            model_name='comment',
            name='is_markdown',
        ),
        migrations.AddField(
            model_name='comment',
            name='contentType',
            field=models.CharField(default=b' ', max_length=50),
        ),
        migrations.CreateModel(
            name='ForeignHost',
            fields=[
                ('username', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=60)),
                ('url', models.CharField(max_length=500, serialize=False, primary_key=True)),
                ('foreign_username', models.ForeignKey(default='', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Git_Post',
            fields=[
                ('title', models.CharField(default=b' ', max_length=500)),
                ('date', models.CharField(default=b' ', max_length=500)),
                ('link', models.CharField(default=b' ', max_length=500)),
                ('primary_key', models.UUIDField(default=uuid.uuid4, serialize=False, primary_key=True)),
            ],
        ),
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
    ]
