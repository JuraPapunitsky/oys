# coding=utf-8

from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       # Библиотеки
                       url(r'^grappelli/', include('grappelli.urls')),
                       url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^i18n/', include('django.conf.urls.i18n', namespace='i18n')),

                       # Проект
                       url(r'^', include('common.urls', namespace='common')),
                       url(r'^lib/', include('lib.urls', namespace='lib')),
                       url(r'^account/', include('account.urls', namespace='account')),
                       url(r'^calculator/', include('calculator.urls', namespace='calculator')),
                       url(r'^sale/', include('sale.urls', namespace='sale')),
)