# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0003_auto_20170217_2042'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transporttype',
            name='tag_value',
        ),
        migrations.AddField(
            model_name='transporttype',
            name='description',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
