# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0019_travelcontract_insured_days'),
    ]

    operations = [
        migrations.AddField(
            model_name='travelcontract',
            name='traveller_gender',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='gender', choices=[(1, 'Male'), (2, 'Female')]),
        ),
    ]
