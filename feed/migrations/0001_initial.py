# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.UUIDField(serialize=False, editable=False, primary_key=True)),
                ('displayName', models.CharField(max_length=60)),
                ('bio', models.CharField(default=b' ', max_length=1000)),
                ('host', models.URLField(max_length=500)),
                ('github', models.CharField(default=b' ', max_length=30)),
                ('github_flag', models.BooleanField(default=False)),
                ('admin_auth', models.BooleanField(default=False)),
                ('url', models.CharField(default=b' ', max_length=500)),
                ('email', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('author_name', models.CharField(default=b' ', max_length=1000)),
                ('comment', models.CharField(max_length=1000)),
                ('contentType', models.CharField(default=b' ', max_length=50)),
                ('published', models.DateTimeField(default=django.utils.timezone.now)),
                ('image', models.ImageField(upload_to=b'', blank=True)),
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
        migrations.CreateModel(
            name='ForeignHost',
            fields=[
                ('username', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=60)),
                ('url', models.CharField(max_length=500, serialize=False, primary_key=True)),
                ('foreign_username', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('primary_key', models.UUIDField(default=uuid.uuid4, serialize=False, primary_key=True)),
                ('follower_host', models.URLField(max_length=500)),
                ('follower_id', models.UUIDField()),
                ('followed_host', models.URLField(max_length=500)),
                ('followed_id', models.UUIDField()),
            ],
        ),
        migrations.CreateModel(
            name='Git_Post',
            fields=[
                ('primary_key', models.UUIDField(default=uuid.uuid4, serialize=False, primary_key=True)),
                ('title', models.CharField(default=b' ', max_length=500)),
                ('date', models.CharField(default=b' ', max_length=500)),
                ('link', models.CharField(default=b' ', max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Img',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('actual_image', models.ImageField(default=b'images/None/none.jpg', upload_to=b'images/')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('published', models.DateTimeField(default=django.utils.timezone.now)),
                ('content', models.CharField(max_length=1000)),
                ('contentType', models.CharField(default=b' ', max_length=50)),
                ('visibility', models.CharField(max_length=20)),
                ('image', models.ImageField(upload_to=b'', blank=True)),
                ('title', models.CharField(default=b' ', max_length=50)),
                ('source', models.URLField(default=b' ')),
                ('origin', models.URLField(default=b' ')),
                ('description', models.CharField(default=b' ', max_length=150)),
                ('count', models.IntegerField(default=0)),
                ('categories', models.CharField(default=b' ', max_length=1000)),
                ('author', models.ForeignKey(to='feed.Author')),
            ],
        ),
        migrations.AddField(
            model_name='img',
            name='parent_post',
            field=models.ForeignKey(default=None, to='feed.Post'),
        ),
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(to='feed.CommentAuthor'),
        ),
        migrations.AddField(
            model_name='comment',
            name='post_id',
            field=models.ForeignKey(to='feed.Post'),
        ),
    ]
