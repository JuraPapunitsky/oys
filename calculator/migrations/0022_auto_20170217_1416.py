# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0021_auto_20150903_1743'),
    ]

    operations = [
        migrations.AddField(
            model_name='healthcontract',
            name='d_payment',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='healthcontract',
            name='s_payment',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='healthcontract',
            name='s_premium',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='propertycontract',
            name='d_payment',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='propertycontract',
            name='s_payment',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='propertycontract',
            name='s_premium',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='travelcontract',
            name='d_payment',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='travelcontract',
            name='s_payment',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='travelcontract',
            name='s_premium',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='vehiclecontract',
            name='d_payment',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='vehiclecontract',
            name='s_payment',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='vehiclecontract',
            name='s_premium',
            field=models.FloatField(null=True),
        ),
    ]
