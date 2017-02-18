# coding=utf-8

from django.conf.urls import patterns, url
from django.contrib.auth import views as auth_views

from .forms import RestorePasswordForm
from account import views

urlpatterns = patterns('account.views',

                       url(r'^register/$', view=views.RegisterView.as_view(), name='register'),
                       url(r'^login/(?P<step>(get_password|login_by_password))/$', view=views.LoginView.as_view(), name='login'),

                       # Профиль
                       # url(r'^profile/$', view=views.Profile.as_view(), name='profile'),
                       # url(r'^profile/edit/$', view=views.ProfileEdit.as_view(), name='profile_edit'),

                       # # Восстановление пароля
                       # url(r'^password_restore/$',
                       #     view=auth_views.password_reset,
                       #     name='password_restore',
                       #     kwargs={'template_name': 'account/auth/password_restore.html',
                       #             'email_template_name': 'account/auth/password_restore_email.html',
                       #             'post_reset_redirect' : '/password_restore_done/',
                       #             'password_reset_form': RestorePasswordForm
                       #             }),

                       # # Восстановление успешно
                       # url(r'^password_restore_done/$',
                       #     view=auth_views.password_reset_done,
                       #     name='password_restore_done',
                       #     kwargs={'template_name': 'account/auth/password_restore_done.html'}),

                       # # Подтверждение токена и ввод нового пароля
                       # url(r'^password_restore_confirm/(?P<uidb64>[0-9A-Za-z]{1,13})/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
                       #     view=auth_views.password_reset_confirm,
                       #     name='password_restore_confirm',
                       #     kwargs={'template_name': 'account/auth/password_restore_confirm.html'}),

                       # # Сообщение о смене пароля
                       # url(r'^password_reset_complete/$',
                       #     view=auth_views.password_reset_complete,
                       #     name='password_reset_complete',
                       #     kwargs={'template_name': 'account/auth/password_reset_complete.html'}),

                       

              )
