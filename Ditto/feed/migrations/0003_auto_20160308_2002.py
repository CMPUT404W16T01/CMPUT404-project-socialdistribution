# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0002_author_admin_auth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='bio',
            field=models.CharField(default=b'', max_length=1000),
        ),
        migrations.AlterField(
            model_name='author',
            name='github_account',
            field=models.CharField(default=b'', max_length=30),
        ),
    ]
