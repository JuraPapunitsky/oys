# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0010_auto_20150626_1301'),
    ]

    operations = [
        migrations.AddField(
            model_name='propertycontract',
            name='is_completed',
            field=models.BooleanField(default=False, verbose_name='completed', db_index=True, editable=False),
        ),
        migrations.AddField(
            model_name='vehiclecontract',
            name='is_completed',
            field=models.BooleanField(default=False, verbose_name='completed', db_index=True, editable=False),
        ),
    ]
