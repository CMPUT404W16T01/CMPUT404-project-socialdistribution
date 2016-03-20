# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-11 02:39
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('user_id', models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('display_name', models.CharField(max_length=60)),
                ('bio', models.CharField(default=b' ', max_length=1000)),
                ('host', models.URLField(max_length=500)),
                ('github_account', models.CharField(default=b' ', max_length=30)),
                ('github_flag', models.BooleanField(default=False)),
                ('admin_auth', models.BooleanField(default=False)),
                ('email', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('comment_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('body', models.CharField(max_length=1000)),
                ('is_markdown', models.BooleanField(default=False)),
                ('date_published', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(blank=True, upload_to=b'')),
                ('author_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feed.Author')),
            ],
        ),
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('follower_id', models.UUIDField(primary_key=True, serialize=False)),
                ('followed_id', models.UUIDField()),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('post_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date_published', models.DateTimeField(auto_now=True)),
                ('body', models.CharField(max_length=1000)),
                ('is_markdown', models.BooleanField(default=False)),
                ('visibility', models.CharField(max_length=20)),
                ('image', models.ImageField(blank=True, upload_to=b'')),
                ('title', models.CharField(default=b' ', max_length=50)),
                ('source', models.URLField(default=b' ')),
                ('origin', models.URLField(default=b' ')),
                ('description', models.CharField(default=b' ', max_length=150)),
                ('comment_count', models.IntegerField(default=0)),
                ('categories', models.CharField(default=b' ', max_length=1000)),
                ('author_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feed.Author')),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='post_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feed.Post'),
        ),
    ]