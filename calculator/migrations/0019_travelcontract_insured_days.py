# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0018_auto_20150901_1300'),
    ]

    operations = [
        migrations.AddField(
            model_name='travelcontract',
            name='insured_days',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
    ]
