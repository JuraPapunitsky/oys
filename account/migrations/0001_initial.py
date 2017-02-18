# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('phone', models.CharField(unique=True, max_length=200, verbose_name='Phone')),
                ('email', models.EmailField(max_length=75, unique=True, null=True, verbose_name='Email', blank=True)),
                ('fin', models.CharField(max_length=30, unique=True, null=True, verbose_name='FIN', blank=True)),
                ('last_name', models.CharField(max_length=30, null=True, verbose_name='Last name', blank=True)),
                ('first_name', models.CharField(max_length=30, null=True, verbose_name='First name', blank=True)),
                ('middle_name', models.CharField(max_length=30, null=True, verbose_name='Middle name', blank=True)),
                ('birthday', models.DateField(null=True, blank=True)),
                ('gender', models.PositiveSmallIntegerField(default=1, choices=[(1, '\u041c\u0443\u0436\u0441\u043a\u043e\u0439'), (2, '\u0416\u0435\u043d\u0441\u043a\u0438\u0439')])),
                ('address', models.CharField(max_length=30, null=True, blank=True)),
                ('address_index', models.CharField(max_length=30, null=True, blank=True)),
                ('is_staff', models.BooleanField(default=False, verbose_name='\u041f\u0435\u0440\u0441\u043e\u043d\u0430\u043b')),
                ('is_active', models.BooleanField(default=True, verbose_name='\u0410\u043a\u0442\u0438\u0432\u0435\u043d')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430 \u0440\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u0438')),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'ordering': ['last_name', 'first_name', 'middle_name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CallMe',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('d_create', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=50)),
                ('d_call', models.DateField()),
                ('d_call_from', models.TimeField()),
                ('d_call_to', models.TimeField()),
                ('reason', models.PositiveSmallIntegerField(choices=[(1, 'Reason 1'), (2, 'Reason 2')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
