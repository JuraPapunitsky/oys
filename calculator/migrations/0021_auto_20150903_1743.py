# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0020_travelcontract_traveller_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='travelcontract',
            name='rest_term_year',
            field=models.BooleanField(default=False, verbose_name='one year contract'),
        ),
        migrations.AddField(
            model_name='travelcontract',
            name='traveller_address',
            field=models.CharField(max_length=250, null=True, verbose_name='traveller address', blank=True),
        ),
        migrations.AddField(
            model_name='travelcontract',
            name='traveller_city',
            field=models.PositiveIntegerField(null=True, verbose_name='traveller city', blank=True),
        ),
        migrations.AddField(
            model_name='travelcontract',
            name='traveller_pin',
            field=models.CharField(max_length=10, null=True, verbose_name='traveller pin', blank=True),
        ),
    ]
