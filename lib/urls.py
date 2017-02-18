# coding=utf-8

from django.conf.urls import patterns, url
from django.contrib.auth import views as auth_views
from .forms import CustomPasswordResetForm

urlpatterns = patterns(
    'lib.views',

    # Управление учетными записями
    url(r'^login/$',
       view=auth_views.login,
       name='login',
       kwargs={'template_name': 'lib/login.html'}),
    url(r'^logout/$',
       view=auth_views.logout,
       name='logout',
       kwargs={'template_name': 'lib/logout.html'}),

    # Смена пароля
    url(r'^password_change/$', view=auth_views.password_change,
       name='password_change',
       kwargs={'template_name': 'lib/password_change.html',
               'post_change_redirect': '/password_change_done/'}),
    url(r'^password_change_done/$',
       view=auth_views.password_change_done,
       name='password_change_done',
       kwargs={'template_name': 'lib/password_change_done.html'}),

    # Сброс и восстановление пароля
    url(r'^password_reset/$',
        view=auth_views.password_reset,
        name='password_reset',
        kwargs={
            'template_name': 'lib/password_reset.html',
            'email_template_name': 'lib/password_reset_email.html',
            'post_reset_redirect': '/password_reset_done/',
            'password_reset_form': CustomPasswordResetForm,
        }),
    url(r'^password_reset_done/$',
       view=auth_views.password_reset_done,
       name='password_reset_done',
       kwargs={'template_name': 'lib/password_reset_done.html'}),
    url(r'^password_reset_confirm/(?P<uidb64>[0-9A-Za-z]{1,13})/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
       view=auth_views.password_reset_confirm,
       name='base_password_reset_confirm',
       kwargs={'template_name': 'lib/password_reset_confirm.html'}),
    url(r'^password_reset_complete/$',
       view=auth_views.password_reset_complete,
       name='password_reset_complete',
       kwargs={'template_name': 'lib/password_reset_complete.html'}),


    # Поставщиики данных для виджетов
    url(r'^forms_widget_autocomplete/', view='forms_widget_autocomplete',
       name='forms_widget_autocomplete'),

    url(r'^tree_widget/(?P<application>\w+)/(?P<model_name>\w+)/$',
       view='tree_widget', name='tree_widget'),

    # url(r'^autocomplete_widget/(?P<application>\w+)/(?P<model_name>\w+)/$',
    #     view=views.autocomplete_widget, name='autocomplete_widget'),

    # Документция по БД
    url(r'^documentation/$', view='db_documentation', name='db_documentation'),

    url(r'^set_lang/(?P<code>\w{2})/$', view='set_lang', name='set_lang'),

    # Скрипт закрытия модального окна и обновления opener
    # Для переадресации сюда по success_url
    url(r'^close_modal_window/$', view='close_modal_window', name='close_modal_window'),
    url(r'^close_modal_window_no_reload/$', view='close_modal_window_no_reload', name='close_modal_window_no_reload'),



)
