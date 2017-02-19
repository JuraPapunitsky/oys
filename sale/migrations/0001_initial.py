# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BearingCapacity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bearing_capacity', models.CharField(max_length=200)),
                ('premium', models.FloatField(max_length=10)),
                ('tag_value', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='CarManufacturer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('tag_value', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='CarModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('model', models.CharField(max_length=200)),
                ('brand', models.ForeignKey(to='sale.CarManufacturer')),
            ],
        ),
        migrations.CreateModel(
            name='CarTypeCarModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('car_model', models.ForeignKey(to='sale.CarModel')),
            ],
        ),
        migrations.CreateModel(
            name='ClientData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('registration_numbe', models.CharField(max_length=200)),
                ('car_engine', models.FloatField(max_length=20)),
                ('car_size', models.FloatField(max_length=200)),
                ('car_weight', models.FloatField(max_length=20)),
                ('pin_code', models.CharField(max_length=20)),
                ('driver_license_series', models.CharField(max_length=20)),
                ('driver_license_number', models.CharField(max_length=20)),
                ('start_date', models.DateField()),
                ('phone', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('prem', models.FloatField(verbose_name=10)),
                ('car_manufacturer', models.ForeignKey(to='sale.CarManufacturer')),
                ('car_model', models.ForeignKey(to='sale.CarModel')),
            ],
        ),
        migrations.CreateModel(
            name='DocType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('doc_type', models.CharField(max_length=200)),
                ('premium', models.FloatField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='EngineCapacity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('engine_capacity', models.CharField(max_length=200)),
                ('premium', models.FloatField(max_length=10)),
                ('tag_value', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='PassengerSeats',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('passenger_seats', models.CharField(max_length=200)),
                ('premium', models.FloatField(max_length=10)),
                ('tag_value', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='PersonType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('person_type', models.CharField(max_length=200)),
                ('premium', models.FloatField(max_length=10)),
                ('tag_value', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Territory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('tag_value', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TransportType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('transport_type', models.CharField(max_length=200)),
                ('premium', models.FloatField(max_length=10)),
                ('description', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='clientdata',
            name='car_type',
            field=models.ForeignKey(to='sale.TransportType'),
        ),
        migrations.AddField(
            model_name='clientdata',
            name='person_type',
            field=models.ForeignKey(to='sale.PersonType'),
        ),
        migrations.AddField(
            model_name='clientdata',
            name='territory',
            field=models.ForeignKey(to='sale.Territory'),
        ),
        migrations.AddField(
            model_name='cartypecarmodel',
            name='transport_type',
            field=models.ForeignKey(to='sale.TransportType'),
        ),
    ]
