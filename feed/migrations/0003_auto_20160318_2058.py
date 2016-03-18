# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0002_auto_20160317_2155'),
    ]

    operations = [
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
        migrations.RenameField(
            model_name='post',
            old_name='body',
            new_name='content',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='comment_count',
            new_name='count',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='post_id',
            new_name='id',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='date_published',
        ),
        migrations.RemoveField(
            model_name='post',
            name='author_name',
        ),
        migrations.RemoveField(
            model_name='post',
            name='date_published',
        ),
        migrations.AddField(
            model_name='comment',
            name='published',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='post',
            name='published',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='author',
            name='url',
            field=models.CharField(default=b' ', max_length=500),
        ),
    ]
