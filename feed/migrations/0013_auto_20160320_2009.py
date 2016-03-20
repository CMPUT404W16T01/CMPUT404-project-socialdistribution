# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0012_auto_20160320_1930'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='author_id',
            new_name='author',
        ),
    ]
