# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('lib', '0006_smstask_task_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logaccess',
            name='remote_addr',
            field=models.GenericIPAddressField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='logaccess',
            name='user',
            field=models.ForeignKey(related_name='log_access', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='smstask',
            name='task_type',
            field=models.CharField(max_length=50),
            preserve_default=True,
        ),
    ]
