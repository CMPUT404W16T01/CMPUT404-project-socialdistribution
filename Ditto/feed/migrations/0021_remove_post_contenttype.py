# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0020_auto_20160309_1852'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='contentType',
        ),
    ]
