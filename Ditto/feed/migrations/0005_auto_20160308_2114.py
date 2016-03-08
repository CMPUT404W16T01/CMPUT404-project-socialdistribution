# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0004_auto_20160308_2004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='user_id',
            field=models.UUIDField(serialize=False, editable=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='comment_id',
            field=models.UUIDField(serialize=False, editable=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='post_id',
            field=models.UUIDField(serialize=False, editable=False, primary_key=True),
        ),
    ]
