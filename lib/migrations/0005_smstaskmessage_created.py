# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lib', '0004_auto_20150720_1722'),
    ]

    operations = [
        migrations.AddField(
            model_name='smstaskmessage',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='created', db_index=True),
            preserve_default=True,
        ),
    ]
