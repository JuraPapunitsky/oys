# coding=utf-8

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from account import models


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'fin', 'email', 'first_name', 'last_name', 'is_active')
    list_filter = ('is_superuser', 'is_staff')
    readonly_fields = ('date_joined',)
    fieldsets = (
        (None, {'fields': ('fin', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'middle_name', 'last_name', 'gender', 'email', 'phone', )}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    ordering = ('last_name', 'first_name', 'middle_name')


admin.site.register(models.User, CustomUserAdmin)