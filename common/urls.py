# coding=utf-8

from django.conf.urls import patterns, url
from django.contrib.auth import views as auth_views

from common import views

urlpatterns = patterns('common.views',

                       # Перезвоните мне
                       url(r'^call_me_handler/$', view=views.CallMeHandlerView.as_view(), name='call_me_handler'),
                       url(r'^ask_question/$', view=views.QuestionProcessView.as_view(), name='ask_question'),
                       url(r'^make_complaint/$', view=views.ComplaintProcessView.as_view(), name='make_complaint'),

                       # url(r'^logout/$',
                       #     view=auth_views.logout,
                       #     name='logout',
                       #     kwargs={'template_name': 'account/auth/logout.html'}),
)
