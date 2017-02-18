# coding=utf-8

from django.contrib import admin

from common import models


class CallMeAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone', 'name', 'd_call_from', 'd_call_to', 'reason')
    list_search = ('phone', 'name',)

admin.site.register(models.CallMe, CallMeAdmin)
