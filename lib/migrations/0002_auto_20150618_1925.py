# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('lib', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logaccess',
            name='user',
            field=models.ForeignKey(related_name='log_access', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
