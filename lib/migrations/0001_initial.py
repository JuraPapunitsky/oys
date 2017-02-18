# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LogAccess',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('d_create', models.DateTimeField(auto_now_add=True)),
                ('remote_addr', models.IPAddressField()),
                ('remote_host', models.CharField(max_length=100, null=True, blank=True)),
                ('http_referer', models.CharField(max_length=1000, null=True, blank=True)),
                ('path', models.CharField(max_length=1000, null=True, blank=True)),
                ('post', models.TextField(null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
