# coding=utf-8

u""" 
Примеси для views
"""

import json

from django.contrib import messages
from django.http import HttpResponse

from lib.utils import get_trace


class FormProcessMixin(object):
    u''' Обработка отправки формы '''

    def post(self, request, *args, **kwargs):
        
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        if form.errors:
            messages.error(request, unicode(form.errors))
        return self.get(request, *args, **kwargs)

    def form_valid(self, form):
        raise NotImplemented


class AjaxResponseMixin(object):
    u''' Обрабатывает возврат параметров через Ajax '''

    def get(self, request, *args, **kwargs):
        try:
            result_dict = {"error": None, "result": self.process_ajax()}
        except Exception as e:
            exception_class = type(e).__name__
            result_dict = {"error": unicode(e), 'exception_class': exception_class}
        
        return HttpResponse(json.dumps(result_dict), content_type="application/json;charset=utf-8")

    def process_ajax(self):
        raise NotImplemented

