# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lib', '0002_auto_20150618_1925'),
    ]

    operations = [
        migrations.CreateModel(
            name='SmsTask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('internal_id', models.CharField(db_index=True, max_length=36, null=True, verbose_name='internal id', blank=True)),
                ('external_id', models.CharField(db_index=True, max_length=50, null=True, verbose_name='external task id', blank=True)),
                ('sender_title', models.CharField(unique=True, max_length=100, verbose_name='sender title')),
            ],
        ),
        migrations.CreateModel(
            name='SmsTaskMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('msisdn', models.CharField(max_length=12, verbose_name=b'ISDN', db_index=True)),
                ('message', models.TextField(null=True, verbose_name='message', blank=True)),
                ('status', models.PositiveIntegerField(default=1, verbose_name='status', choices=[(1, 'Message is queued'), (2, 'Message was successfully delivered'), (3, 'Message delivery failed'), (4, 'Message was removed from list'), (5, 'System error')])),
                ('status_change', models.DateTimeField(auto_now_add=True, verbose_name='last status change')),
                ('task', models.ForeignKey(to='lib.SmsTask')),
            ],
        ),
    ]
