# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0027_auto_20160316_2122'),
    ]

    operations = [
        migrations.RenameField(
            model_name='author',
            old_name='id',
            new_name='user_id',
        ),
    ]
