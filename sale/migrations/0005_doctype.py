# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0004_auto_20170217_2315'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('doc_type', models.CharField(max_length=200)),
                ('premium', models.FloatField(max_length=10)),
            ],
        ),
    ]
