# coding=utf-8

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import PasswordResetForm

from account.models import User


class RegisterForm(forms.Form):
    u""" Форма регистрации """

    phone = forms.CharField(label=_('Phone'))
    email = forms.EmailField(label=_('Email'))
    fin = forms.CharField(label=_('FIN'))
    last_name = forms.CharField(label=_('Last name'))
    first_name = forms.CharField(label=_('First name'))
    middle_name = forms.CharField(label=_('Middle name'))

    def clean_phone(self):
        phone = self.cleaned_data['phone']

        if User.objects.filter(phone=phone).exists():
            raise forms.ValidationError(_(u'User with phone exists'))

        return phone

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_(u'User with email exists'))

        return email


class RestorePasswordForm(PasswordResetForm):
    u""" Восстановление пароля """
    phone = forms.CharField(label=_('Phone'))

    def clean(self):
        cleaned_data = super(RestorePasswordForm, self).clean()

        phone = cleaned_data.get('phone')
        email = cleaned_data.get('email')

        if phone and email and not User.objects.filter(email=email, phone=phone).exists():
            raise forms.ValidationError(_(u'User with email and phone not exists'))


class LoginFormStep1(forms.Form):
    phone = forms.CharField(required=True)


class LoginFormStep2(forms.Form):
    phone = forms.CharField(required=True)
    password = forms.CharField(required=True)





