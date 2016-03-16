# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0028_auto_20160316_2125'),
    ]

    operations = [
        migrations.RenameField(
            model_name='author',
            old_name='user_id',
            new_name='id',
        ),
    ]
