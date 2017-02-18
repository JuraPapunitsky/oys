# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0003_auto_20150603_1405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehiclecontract',
            name='ad1_birthday',
            field=models.DateField(null=True, verbose_name='birthday', blank=True),
        ),
        migrations.AlterField(
            model_name='vehiclecontract',
            name='ad1_country',
            field=models.PositiveIntegerField(null=True, verbose_name='country', blank=True),
        ),
        migrations.AlterField(
            model_name='vehiclecontract',
            name='ad1_email',
            field=models.EmailField(max_length=254, null=True, verbose_name='email', blank=True),
        ),
        migrations.AlterField(
            model_name='vehiclecontract',
            name='ad1_fname',
            field=models.CharField(max_length=50, null=True, verbose_name='first name', blank=True),
        ),
        migrations.AlterField(
            model_name='vehiclecontract',
            name='ad1_gender',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='gender', blank=True),
        ),
        migrations.AlterField(
            model_name='vehiclecontract',
            name='ad1_index',
            field=models.CharField(max_length=6, null=True, verbose_name='postal index (ZIP)', blank=True),
        ),
        migrations.AlterField(
            model_name='vehiclecontract',
            name='ad1_lname',
            field=models.CharField(max_length=50, null=True, verbose_name='last name', blank=True),
        ),
        migrations.AlterField(
            model_name='vehiclecontract',
            name='ad1_mname',
            field=models.CharField(max_length=50, null=True, verbose_name='middle name', blank=True),
        ),
        migrations.AlterField(
            model_name='vehiclecontract',
            name='ad1_phone',
            field=models.CharField(max_length=12, null=True, verbose_name='phone', blank=True),
        ),
        migrations.AlterField(
            model_name='vehiclecontract',
            name='ad1_pin',
            field=models.CharField(max_length=9, null=True, verbose_name='PIN', blank=True),
        ),
        migrations.AlterField(
            model_name='vehiclecontract',
            name='ad2_birthday',
            field=models.DateField(null=True, verbose_name='birthday', blank=True),
        ),
        migrations.AlterField(
            model_name='vehiclecontract',
            name='ad2_country',
            field=models.PositiveIntegerField(null=True, verbose_name='country', blank=True),
        ),
        migrations.AlterField(
            model_name='vehiclecontract',
            name='ad2_email',
            field=models.EmailField(max_length=254, null=True, verbose_name='email', blank=True),
        ),
        migrations.AlterField(
            model_name='vehiclecontract',
            name='ad2_fname',
            field=models.CharField(max_length=50, null=True, verbose_name='first name', blank=True),
        ),
        migrations.AlterField(
            model_name='vehiclecontract',
            name='ad2_gender',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='gender', blank=True),
        ),
        migrations.AlterField(
            model_name='vehiclecontract',
            name='ad2_index',
            field=models.CharField(max_length=6, null=True, verbose_name='postal index (ZIP)', blank=True),
        ),
        migrations.AlterField(
            model_name='vehiclecontract',
            name='ad2_lname',
            field=models.CharField(max_length=50, null=True, verbose_name='last name', blank=True),
        ),
        migrations.AlterField(
            model_name='vehiclecontract',
            name='ad2_mname',
            field=models.CharField(max_length=50, null=True, verbose_name='middle name', blank=True),
        ),
        migrations.AlterField(
            model_name='vehiclecontract',
            name='ad2_phone',
            field=models.CharField(max_length=12, null=True, verbose_name='phone', blank=True),
        ),
        migrations.AlterField(
            model_name='vehiclecontract',
            name='ad2_pin',
            field=models.CharField(max_length=9, null=True, verbose_name='PIN', blank=True),
        ),
        migrations.AlterField(
            model_name='vehiclecontract',
            name='ins_index',
            field=models.CharField(max_length=6, verbose_name='postal index (ZIP)'),
        ),
        migrations.AlterField(
            model_name='vehiclecontract',
            name='owner_birthday',
            field=models.DateField(null=True, verbose_name='birthday', blank=True),
        ),
        migrations.AlterField(
            model_name='vehiclecontract',
            name='owner_country',
            field=models.PositiveIntegerField(null=True, verbose_name='country', blank=True),
        ),
        migrations.AlterField(
            model_name='vehiclecontract',
            name='owner_email',
            field=models.EmailField(max_length=254, null=True, verbose_name='email', blank=True),
        ),
        migrations.AlterField(
            model_name='vehiclecontract',
            name='owner_fname',
            field=models.CharField(max_length=50, null=True, verbose_name='first name', blank=True),
        ),
        migrations.AlterField(
            model_name='vehiclecontract',
            name='owner_gender',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='gender', blank=True),
        ),
        migrations.AlterField(
            model_name='vehiclecontract',
            name='owner_index',
            field=models.CharField(max_length=6, null=True, verbose_name='postal index (ZIP)', blank=True),
        ),
        migrations.AlterField(
            model_name='vehiclecontract',
            name='owner_lname',
            field=models.CharField(max_length=50, null=True, verbose_name='last name', blank=True),
        ),
        migrations.AlterField(
            model_name='vehiclecontract',
            name='owner_mname',
            field=models.CharField(max_length=50, null=True, verbose_name='middle name', blank=True),
        ),
        migrations.AlterField(
            model_name='vehiclecontract',
            name='owner_phone',
            field=models.CharField(max_length=12, null=True, verbose_name='phone', blank=True),
        ),
        migrations.AlterField(
            model_name='vehiclecontract',
            name='owner_pin',
            field=models.CharField(max_length=9, null=True, verbose_name='PIN', blank=True),
        ),
    ]
