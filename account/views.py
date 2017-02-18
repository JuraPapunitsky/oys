# coding=utf-8

import hashlib
from datetime import datetime

from django.shortcuts import render
from django.template.loader import render_to_string
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
from django.db import transaction
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import authenticate, login

from lib.utils import send_mail
from lib.cbv_mixins import AjaxResponseMixin

from django.views.generic import View, TemplateView, FormView


from .models import User
from account import forms


class RegisterView(FormView):
    pass


class LoginView(AjaxResponseMixin, View):
    u"""
    Вход в систему. Осуществляется в виде 2-х этапной авторизации
    Сначала человек запрашивает отправку одноразового кода на телефон.
    Мы генерируем для него пароль и пробиваем его в объекте User
    потом отправляет этот код с номером телефона вместе.
    Если все ок - авторизуем его через стандартный AUTHENTICATION_BACKEND
    """

    def process_ajax(self):
        data = self.request.GET
        step = self.kwargs['step']
        if step == 'get_password':
            user = User.objects.get(phone=data.get('phone'))
            user.send_password()

        elif step == 'login_by_password':
            phone = data['phone']
            password = data['password']
            
            user = authenticate(phone=phone, password=password)
            if user is not None and user.is_active:
                login(self.request, user)
                return 'success'
            else:
                return 'not_found'


# def register(request):
#     u""" 
#     Регистрация нового человека 
#     Создаем пользователя по запросу 
#     и отправляем ему оповещение с паролем
#     """
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             data = form.cleaned_data
#             user = User(phone=data['phone'],
#                         email=data['email'],
#                         fin=data['fin'],
#                         last_name=data['last_name'],
#                         first_name=data['first_name'],
#                         middle_name=data['middle_name'],
#                         last_login=timezone.now())

#             md5 = hashlib.md5()
#             md5.update(data['phone'])
#             md5.update(str(datetime.utcnow()))

#             password = md5.hexdigest()[0:8]
#             user.set_password(password)
#             user.save()

#             user.notify_register(password)
#             messages.success(request, _(u'Поздравляем. Вы зарегистрированы. Дождитесь сообщения с паролем'))

#             return HttpResponseRedirect('/')

#     else:
#         form = RegisterForm()

    # return render(request, 'account/register.html', {'form': form})

