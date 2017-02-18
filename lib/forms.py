# coding=utf-8

from django.forms import Form, CharField, PasswordInput, ValidationError
from django.contrib import auth
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import PasswordResetForm, get_user_model

User = get_user_model()

class LoginForm(Form):
    u""" Форма входа """

    username = CharField(max_length=50, label=_('Username'))
    password = CharField(max_length=50, label=_('Password'),
                         widget=PasswordInput())

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()

        if 'username' in cleaned_data and 'password' in cleaned_data:
            user = auth.authenticate(username=cleaned_data['username'],
                                     password=cleaned_data['password'])
            if user is None or not user.is_active:
                raise ValidationError(_(u'No active user'))

        return cleaned_data


class CustomPasswordResetForm(PasswordResetForm):

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            raise ValidationError(u'Пользователь не найден')
        return email
