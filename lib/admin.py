# coding=utf-8
from django.contrib import admin
from lib.models import SmsTask, SmsTaskMessage


class SmsTaskMessageInline(admin.TabularInline):
    model = SmsTaskMessage
    extra = 0
    readonly_fields = ('msisdn', 'message', 'status', 'status_change')


class SmsTaskAdmin(admin.ModelAdmin):
    list_display = ('internal_id', 'external_id', 'sender_title')
    readonly_fields = ('internal_id', 'external_id', 'sender_title')
    inlines = [SmsTaskMessageInline, ]

admin.site.register(SmsTask, SmsTaskAdmin)


class SmsMessageAdmin(admin.ModelAdmin):
    list_display = ('msisdn', 'message', 'status', 'status_change')
    readonly_fields = ('msisdn', 'message', 'status', 'status_change')
    search_fields = ('msisdn', )
    list_filter = ('status', )

admin.site.register(SmsTaskMessage, SmsMessageAdmin)

