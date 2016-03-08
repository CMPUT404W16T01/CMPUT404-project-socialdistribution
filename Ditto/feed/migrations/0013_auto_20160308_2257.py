# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0012_auto_20160308_2252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='email',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
    ]
