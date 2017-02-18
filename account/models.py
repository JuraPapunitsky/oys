# coding=utf-8

import uuid

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from lib.utils import send_mail

GENDER = ((1, _(u'Мужской')), (2, _(u'Женский')),)


class UserManager(BaseUserManager):
    def create_user(self, phone, password):
        user = self.model(phone=phone.lower())
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, phone, password):
        user = self.create_user(phone=phone, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db, update_fields=('is_superuser', 'is_staff',))

        return user


class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(_('Phone'), max_length=200, unique=True)
    email = models.EmailField(_('Email'), blank=True, null=True, unique=True)
    fin = models.CharField(_('FIN'), max_length=30, blank=True, null=True, unique=True)

    last_name = models.CharField(_('Last name'), max_length=30, blank=True, null=True)
    first_name = models.CharField(_('First name'), max_length=30, blank=True, null=True)
    middle_name = models.CharField(_('Middle name'), max_length=30, blank=True, null=True)

    birthday = models.DateField(blank=True, null=True)
    gender = models.PositiveSmallIntegerField(choices=GENDER, default=1)

    address = models.CharField(max_length=30, blank=True, null=True)
    address_index = models.CharField(max_length=30, blank=True, null=True)

    # Системные
    is_staff = models.BooleanField(u'Персонал', default=False)
    is_active = models.BooleanField(u'Активен', default=True)
    date_joined = models.DateTimeField(u'Дата регистрации', auto_now_add=True)

    objects = UserManager()

    def get_short_name(self):
        return u"%s %s" % (self.last_name, self.first_name)

    def get_full_name(self):
        return u"%s %s %s" % (self.last_name, self.first_name, self.middle_name)

    def send_email(self, subject, message):
        send_mail(subject, message, [self.email])

    # def login_in_user(self):
    #     return mark_safe(u'<a href="%s">Вход</a>' % reverse('account:login_in_user',
    #                                                         kwargs={'user_id': self.id}))

    def notify_register(self, password):
        u""" Отправить оповещение о регистрации """

        msg = render_to_string('account/auth/email_register.html',
                               {'user': self, 'password': password})
        self.send_email(u'[Odlar Yurdu Sigorta Brokeri] Регистрация', msg)

    def generate_password(self):
        u""" Создает случайный пароль и возвращает его """

        password = uuid.uuid1().hex[:16]
        self.set_password(password)
        self.save()
        return password

    def send_password(self):
        u""" Создает одноразовый пароль и отправляет его человеку """
        password = self.generate_password()
        
        # Форматируем в 5c5c-09e3-e9ac-11e4
        password_verbose = '-'.join([password[i:(i+4)] for i in xrange(0, 16, 4)])
        self.send_email('Ваш пароль', password_verbose)

    def __unicode__(self):
        return self.get_short_name()

    USERNAME_FIELD = 'phone'

    class Meta:
        ordering = ['last_name', 'first_name', 'middle_name']




