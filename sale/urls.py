# coding=utf-8

from django.conf.urls import patterns, url
from django.contrib.auth import views as auth_views

from sale import views

urlpatterns = patterns('sale.views',

      url(r'^auto-step-1/$', view=views.auto_step_1, name='step_1'),
      url(r'^auto-step-2/$', view=views.auto_step_2, name='step_2'),
      url(r'^auto-step-3/$', view=views.auto_step_3, name='step_3'),

)
