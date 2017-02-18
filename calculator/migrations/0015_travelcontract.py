# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('calculator', '0014_auto_20150715_1538'),
    ]

    operations = [
        migrations.CreateModel(
            name='TravelContract',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('d_create', models.DateTimeField(auto_now_add=True, verbose_name='creation date', db_index=True)),
                ('is_completed', models.BooleanField(default=False, verbose_name='completed', db_index=True, editable=False)),
                ('is_issued', models.BooleanField(default=False, verbose_name='issued', db_index=True, editable=False)),
                ('step', models.CharField(max_length=50, verbose_name='calculator step')),
                ('substep', models.CharField(max_length=50, verbose_name='calculator sub step')),
                ('layer', models.CharField(max_length=50, verbose_name='calculator layer')),
                ('main_product', models.PositiveSmallIntegerField(null=True, verbose_name='main product ID', blank=True)),
                ('main_product_text', models.CharField(max_length=100, null=True, verbose_name='main product title', blank=True)),
                ('d_start', models.DateField(null=True, verbose_name='contract start date', blank=True)),
                ('term_insurance', models.PositiveSmallIntegerField(null=True, verbose_name='term insurance', blank=True)),
                ('ins_person_pin', models.CharField(max_length=9, null=True, verbose_name='PIN', blank=True)),
                ('ins_person_lname', models.CharField(max_length=50, null=True, verbose_name='last name', blank=True)),
                ('ins_person_fname', models.CharField(max_length=50, null=True, verbose_name='first name', blank=True)),
                ('ins_person_mname', models.CharField(max_length=50, null=True, verbose_name='middle name', blank=True)),
                ('ins_person_gender', models.PositiveSmallIntegerField(default=1, verbose_name='gender', choices=[(1, 'Male'), (2, 'Female')])),
                ('ins_person_birthday', models.DateField(null=True, verbose_name='birthday', blank=True)),
                ('ins_country', models.PositiveIntegerField(null=True, verbose_name='country', blank=True)),
                ('ins_index', models.CharField(max_length=6, null=True, verbose_name='postal index (ZIP)', blank=True)),
                ('ins_city', models.PositiveIntegerField(null=True, verbose_name='city', blank=True)),
                ('ins_city_custom', models.CharField(max_length=50, null=True, verbose_name='city (custom)', blank=True)),
                ('ins_address', models.CharField(max_length=70, null=True, verbose_name='address', blank=True)),
                ('ins_street', models.CharField(max_length=50, null=True, verbose_name='street', blank=True)),
                ('ins_house', models.CharField(max_length=10, null=True, verbose_name='house', blank=True)),
                ('ins_apartment', models.CharField(max_length=10, null=True, verbose_name='apartment', blank=True)),
                ('ins_phone', models.CharField(max_length=12, null=True, verbose_name='phone', blank=True)),
                ('ins_email', models.EmailField(max_length=254, null=True, verbose_name='email', blank=True)),
                ('delivery_type', models.CharField(max_length=10, null=True, verbose_name='delivery type', blank=True)),
                ('delivery_date', models.DateField(null=True, verbose_name='delivery date', blank=True)),
                ('delivery_time', models.IntegerField(blank=True, null=True, verbose_name='delivery time interval', choices=[(1, b'09:00 - 10:00'), (2, b'10:00 - 11:00'), (3, b'11:00 - 12:00'), (4, b'12:00 - 13:00'), (5, b'13:00 - 14:00'), (6, b'14:00 - 15:00'), (7, b'15:00 - 16:00'), (8, b'16:00 - 17:00'), (9, b'17:00 - 18:00'), (10, b'18:00 - 19:00'), (11, b'19:00 - 20:00')])),
                ('delivery_city', models.PositiveIntegerField(null=True, verbose_name='city', blank=True)),
                ('delivery_region', models.CharField(blank=True, max_length=50, null=True, verbose_name='region', choices=[('Bin\u0259q\u0259di', 'Bin\u0259q\u0259di'), ('Yasamal', 'Yasamal'), ('X\u0259tai', 'X\u0259tai'), ('X\u0259z\u0259r', 'X\u0259z\u0259r'), ('N\u0259rimanov', 'N\u0259rimanov'), ('N\u0259simi', 'N\u0259simi'), ('Nizami', 'Nizami'), ('S\u0259bail', 'S\u0259bail'), ('Sabun\xe7u', 'Sabun\xe7u'), ('Suraxan\u0131', 'Suraxan\u0131'), ('Qarada\u011f', 'Qarada\u011f'), ('Pirallah\u0131', 'Pirallah\u0131'), ('Dig\u0259r', 'Dig\u0259r')])),
                ('delivery_street', models.CharField(max_length=50, null=True, verbose_name='street', blank=True)),
                ('delivery_house', models.CharField(max_length=10, null=True, verbose_name='house', blank=True)),
                ('delivery_apartment', models.CharField(max_length=10, null=True, verbose_name='apartment', blank=True)),
                ('delivery_phone', models.CharField(max_length=12, null=True, verbose_name='phone', blank=True)),
                ('delivery_comment', models.TextField(null=True, verbose_name='comments', blank=True)),
                ('delivery_takeout', models.IntegerField(null=True, verbose_name='takeout point', blank=True)),
                ('delivery_email', models.EmailField(max_length=254, null=True, verbose_name='delivery email', blank=True)),
                ('payment_type', models.CharField(blank=True, max_length=10, null=True, verbose_name='payment type', choices=[(b'cash', 'Cash'), (b'epay', 'Online payment')])),
                ('p4_selected', models.BooleanField(default=False, verbose_name='product 4 selected')),
                ('p4_id', models.PositiveIntegerField(null=True, verbose_name='p4 document id', blank=True)),
                ('currency', models.PositiveIntegerField(null=True, verbose_name='currency', blank=True)),
                ('rest_type', models.PositiveIntegerField(null=True, verbose_name='rest type', blank=True)),
                ('countries', models.PositiveIntegerField(null=True, verbose_name='countries', blank=True)),
                ('ins_value', models.PositiveIntegerField(null=True, verbose_name='ins value', blank=True)),
                ('risk_group', models.PositiveIntegerField(null=True, verbose_name='risk group', blank=True)),
                ('d_rest_start', models.DateField(null=True, verbose_name='rest date start', blank=True)),
                ('d_rest_end', models.DateField(null=True, verbose_name='rest date end', blank=True)),
                ('traveller_first_name', models.CharField(max_length=100, null=True, verbose_name='traveller first name', blank=True)),
                ('traveller_last_name', models.CharField(max_length=100, null=True, verbose_name='traveller last name', blank=True)),
                ('traveller_middle_name', models.CharField(max_length=100, null=True, verbose_name='traveller middle name', blank=True)),
                ('traveller_n_passport', models.CharField(max_length=50, null=True, verbose_name='traveller n passport', blank=True)),
                ('traveller_birthday', models.DateField(null=True, verbose_name='traveller birthday', blank=True)),
                ('embassy', models.PositiveIntegerField(null=True, verbose_name='embassy', blank=True)),
                ('country_of_departure', models.PositiveIntegerField(null=True, blank=True)),
                ('departure_type', models.PositiveIntegerField(null=True, blank=True)),
                ('rest_type_extended', models.PositiveIntegerField(null=True, blank=True)),
                ('p4_inscompany', models.PositiveSmallIntegerField(null=True, verbose_name='insurance company', blank=True)),
                ('client', models.ForeignKey(blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='client')),
            ],
            options={
                'verbose_name': 'travel contract',
                'verbose_name_plural': 'travel contracts',
            },
        ),
    ]
