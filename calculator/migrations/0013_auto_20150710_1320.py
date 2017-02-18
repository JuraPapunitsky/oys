# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0012_auto_20150701_1507'),
    ]

    operations = [
        migrations.AlterField(
            model_name='propertycontract',
            name='branch',
            field=models.PositiveIntegerField(null=True, verbose_name='branch', blank=True),
        ),
        migrations.AlterField(
            model_name='propertycontract',
            name='city',
            field=models.PositiveIntegerField(verbose_name='city'),
        ),
        migrations.AlterField(
            model_name='propertycontract',
            name='delivery_city',
            field=models.PositiveIntegerField(null=True, verbose_name='city', blank=True),
        ),
        migrations.AlterField(
            model_name='propertycontract',
            name='ins_city',
            field=models.PositiveIntegerField(null=True, verbose_name='city', blank=True),
        ),
        migrations.AlterField(
            model_name='propertycontract',
            name='ins_country',
            field=models.PositiveIntegerField(null=True, verbose_name='country', blank=True),
        ),
        migrations.AlterField(
            model_name='propertycontract',
            name='ins_person_gender',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='gender', choices=[(1, 'Male'), (2, 'Female')]),
        ),
        migrations.AlterField(
            model_name='propertycontract',
            name='realty_type',
            field=models.PositiveIntegerField(verbose_name='realty type'),
        ),
        migrations.AlterField(
            model_name='propertycontract',
            name='term_insurance',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='term insurance', blank=True),
        ),
        migrations.AlterField(
            model_name='propertycontract',
            name='using_method',
            field=models.PositiveIntegerField(null=True, verbose_name='using method', blank=True),
        ),
        migrations.AlterField(
            model_name='vehiclecontract',
            name='ad1_city',
            field=models.PositiveIntegerField(null=True, verbose_name='city', blank=True),
        ),
        migrations.AlterField(
            model_name='vehiclecontract',
            name='ad1_country',
            field=models.PositiveIntegerField(null=True, verbose_name='country', blank=True),
        ),
        migrations.AlterField(
            model_name='vehiclecontract',
            name='ad2_city',
            field=models.PositiveIntegerField(null=True, verbose_name='city', blank=True),
        ),
        migrations.AlterField(
            model_name='vehiclecontract',
            name='ad2_country',
            field=models.PositiveIntegerField(null=True, verbose_name='country', blank=True),
        ),
        migrations.AlterField(
            model_name='vehiclecontract',
            name='auto_createyear',
            field=models.PositiveIntegerField(null=True, verbose_name='vehicle creation year', blank=True),
        ),
        migrations.AlterField(
            model_name='vehiclecontract',
            name='auto_engine_capacity',
            field=models.PositiveIntegerField(null=True, verbose_name='vehicle engine capacity', blank=True),
        ),
        migrations.AlterField(
            model_name='vehiclecontract',
            name='auto_mark',
            field=models.PositiveIntegerField(verbose_name='vehicle mark'),
        ),
        migrations.AlterField(
            model_name='vehiclecontract',
            name='auto_model',
            field=models.PositiveIntegerField(verbose_name='vehicle model'),
        ),
        migrations.AlterField(
            model_name='vehiclecontract',
            name='auto_payload',
            field=models.PositiveIntegerField(null=True, verbose_name='vehicle payload', blank=True),
        ),
        migrations.AlterField(
            model_name='vehiclecontract',
            name='auto_region',
            field=models.PositiveIntegerField(verbose_name='vehicle registration region'),
        ),
        migrations.AlterField(
            model_name='vehiclecontract',
            name='auto_type',
            field=models.PositiveIntegerField(verbose_name='vehicle type'),
        ),
        migrations.AlterField(
            model_name='vehiclecontract',
            name='cnt_seats',
            field=models.PositiveIntegerField(null=True, verbose_name='vehicle seats', blank=True),
        ),
        migrations.AlterField(
            model_name='vehiclecontract',
            name='delivery_city',
            field=models.PositiveIntegerField(null=True, verbose_name='city', blank=True),
        ),
        migrations.AlterField(
            model_name='vehiclecontract',
            name='ins_city',
            field=models.PositiveIntegerField(null=True, verbose_name='city', blank=True),
        ),
        migrations.AlterField(
            model_name='vehiclecontract',
            name='ins_country',
            field=models.PositiveIntegerField(null=True, verbose_name='country', blank=True),
        ),
        migrations.AlterField(
            model_name='vehiclecontract',
            name='ins_person_gender',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='gender', choices=[(1, 'Male'), (2, 'Female')]),
        ),
        migrations.AlterField(
            model_name='vehiclecontract',
            name='owner_city',
            field=models.PositiveIntegerField(null=True, verbose_name='city', blank=True),
        ),
        migrations.AlterField(
            model_name='vehiclecontract',
            name='owner_country',
            field=models.PositiveIntegerField(null=True, verbose_name='country', blank=True),
        ),
        migrations.AlterField(
            model_name='vehiclecontract',
            name='p11_bank_beneficiary',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='bank', blank=True),
        ),
        migrations.AlterField(
            model_name='vehiclecontract',
            name='p12_bank_beneficiary',
            field=models.PositiveIntegerField(null=True, verbose_name='bank', blank=True),
        ),
        migrations.AlterField(
            model_name='vehiclecontract',
            name='term_insurance',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='term insurance', blank=True),
        ),
    ]
