# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0008_auto_20160308_2225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='user_id',
            field=models.CharField(max_length=40, serialize=False, editable=False, primary_key=True),
        ),
    ]
