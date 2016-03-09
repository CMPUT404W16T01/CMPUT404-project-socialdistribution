# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0016_auto_20160308_2304'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='password',
        ),
    ]
