# coding=utf-8

from django import forms
from django.utils.translation import ugettext_lazy as _

from common.models import CALLME_REASON, RESPONSE_TYPE


class CallMeForm(forms.Form):
    u""" Форма обратной связи """
    name = forms.CharField()
    phone = forms.CharField()
    d_call = forms.DateField()
    d_call_from = forms.TimeField()
    d_call_to = forms.TimeField()
    reason = forms.TypedChoiceField(coerce=int, choices=CALLME_REASON)
    next_url = forms.CharField()


class QuestionForm(forms.Form):
    u""" Форма обратной связи """
    question = forms.CharField()
    last_name = forms.CharField(required=False)
    first_name = forms.CharField()
    middle_name = forms.CharField(required=False)
    phone = forms.CharField(required=False)
    email = forms.EmailField()
    response_type = forms.TypedChoiceField(coerce=str, choices=RESPONSE_TYPE)


class ComplaintForm(forms.Form):
    u""" Форма обратной связи """
    complaint = forms.CharField()
    last_name = forms.CharField(required=False)
    first_name = forms.CharField()
    middle_name = forms.CharField(required=False)
    phone = forms.CharField(required=False)
    email = forms.EmailField()
    response_type = forms.TypedChoiceField(coerce=str, choices=RESPONSE_TYPE)
