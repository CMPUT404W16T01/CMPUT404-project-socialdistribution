# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0003_auto_20160308_2002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='bio',
            field=models.CharField(default=b' ', max_length=1000),
        ),
        migrations.AlterField(
            model_name='author',
            name='github_account',
            field=models.CharField(default=b' ', max_length=30),
        ),
    ]
