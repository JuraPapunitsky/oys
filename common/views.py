# coding=utf-8

from django.template.loader import render_to_string
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
from django.conf import settings
from lib.utils import send_mail
from django.views.generic import FormView


from common import models, forms


class CallMeHandlerView(FormView):
    u"""
    Обработка формы обратного звонка.
    Сохраним в обращение и отправим письмо
    """
    form_class = forms.CallMeForm

    def form_valid(self, form):
        data = form.cleaned_data

        req = models.CallMe(name=data['name'],
                            phone=data['phone'],
                            d_call=data['d_call'],
                            d_call_from=data['d_call_from'],
                            d_call_to=data['d_call_to'],
                            reason=data['reason'])
        req.save()

        send_mail(u'Позвоните мне',
                  render_to_string('common/email/call_me.html', {'call_request': req}),
                  settings.MANAGERS)

        messages.success(self.request, _(u'Request sent. expect an answer'))

        return HttpResponseRedirect(self.request.POST['next_url'])

    def form_invalid(self, form):
        messages.error(self.request, _(u'Request not sent: %(error_message)s') % {'error_message': form.errors})
        return HttpResponseRedirect(self.request.POST['next_url'])


class QuestionProcessView(FormView):
    u"""
    Обработать вопрос из формы обратной связи
    """
    form_class = forms.QuestionForm

    def form_valid(self, form):
        send_mail(u'Задан вопрос на сайте',
                  render_to_string('common/email/question.html', form.cleaned_data),
                  settings.MANAGERS)
        messages.success(self.request, _(u'Request sent. expect an answer'))

        return HttpResponseRedirect(self.request.POST['next_url'])

    def form_invalid(self, form):
        messages.error(self.request, _(u'Request not sent: %(error_message)s') % {'error_message': form.errors})
        return HttpResponseRedirect(self.request.POST['next_url'])


class ComplaintProcessView(FormView):
    u"""
    Обработать жалобу из формы обратной связи
    """
    form_class = forms.ComplaintForm

    def form_valid(self, form):
        send_mail(u'Создана жалоба на сайте',
                  render_to_string('common/email/complaint.html', form.cleaned_data),
                  settings.MANAGERS)
        messages.success(self.request, _(u'Request sent. expect an answer'))

        return HttpResponseRedirect(self.request.POST['next_url'])

    def form_invalid(self, form):
        messages.error(self.request, _(u'Request not sent: %(error_message)s') % {'error_message': form.errors})
        return HttpResponseRedirect(self.request.POST['next_url'])



