# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0008_auto_20160319_1826'),
    ]

    operations = [
        migrations.CreateModel(
            name='ForeignHost',
            fields=[
                ('username', models.CharField(max_length=20, serialize=False, primary_key=True)),
                ('password', models.CharField(max_length=60)),
                ('url', models.CharField(max_length=500)),
            ],
        ),
    ]
