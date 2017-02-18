# coding=utf-8

u"""
Кастомные поля для форм
"""

from datetime import datetime, time

from django.forms import fields, ValidationError
from django.utils.translation import ugettext_lazy as _
from lib import widgets as widgets_custom
from lib.utils import formset_field_diff


class RangeFieldMixin(object):
    """ set validator for range MultiValueField """

    default_error_messages = {'invalid': u'Date format error',
                              'invalid_order': u'Invalid order',
                              'not_all_filled': u'Not all widget filled'}

    def validate(self, value):
        if (value[0] is None and value[1] is not None) or \
                (value[0] is not None and value[1] is None):
            raise ValidationError(self.default_error_messages['not_all_filled'])

        if value[0] and value[1] and value[0] > value[1]:
            raise ValidationError(self.default_error_messages['invalid_order'])

    def compress(self, data_list):
        return data_list


class DateRangeField(RangeFieldMixin, fields.MultiValueField):
    widget = widgets_custom.DateRangeWidget
    hidden_widget = widgets_custom.DateRangeHiddenWidget

    def __init__(self, input_formats=None, *args, **kwargs):
        errors = self.default_error_messages.copy()
        if 'error_messages' in kwargs:
            errors.update(kwargs['error_messages'])

        localize = kwargs.get('localize', False)

        fields_ = (fields.DateField(input_formats=input_formats,
                                    error_messages={'invalid': errors['invalid']},
                                    localize=localize),
                   fields.DateField(input_formats=input_formats,
                                    error_messages={'invalid': errors['invalid']},
                                    localize=localize), )
        super(DateRangeField, self).__init__(fields_, *args, **kwargs)

    def compress(self, data_list):
        if len(data_list) == 2:
            d_start, d_end = data_list

            if d_start:
                d_start = datetime.combine(d_start, time.min)

            if d_end:
                d_end = datetime.combine(d_end, time.max)

            return (d_start, d_end)

        return data_list


class NumberRangeField(RangeFieldMixin, fields.MultiValueField):
    widget = widgets_custom.NumberRangeWidget
    hidden_widget = widgets_custom.NumberRangeHiddenWidget

    def __init__(self, max_value=None, min_value=None, decimal_places=None, *args, **kwargs):
        errors = self.default_error_messages.copy()
        if 'error_messages' in kwargs:
            errors.update(kwargs['error_messages'])

        localize = kwargs.get('localize', False)

        fields_ = (fields.DecimalField(max_value=max_value,
                                       min_value=min_value,
                                       decimal_places=decimal_places,
                                       error_messages={'invalid': errors['invalid']},
                                       localize=localize),
                   fields.DecimalField(max_value=max_value,
                                       min_value=min_value,
                                       decimal_places=decimal_places,
                                       error_messages={'invalid': errors['invalid']},
                                       localize=localize), )
        super(NumberRangeField, self).__init__(fields_, *args, **kwargs)


class TimeRangeField(RangeFieldMixin, fields.MultiValueField):
    widget = widgets_custom.TimeRangeWidget
    hidden_widget = widgets_custom.TimeRangeHiddenWidget

    def __init__(self, input_formats=None, *args, **kwargs):
        errors = self.default_error_messages.copy()
        if 'error_messages' in kwargs:
            errors.update(kwargs['error_messages'])

        localize = kwargs.get('localize', False)

        fields_ = (fields.TimeField(input_formats=input_formats,
                                    error_messages={'invalid': errors['invalid']},
                                    localize=localize),
                   fields.TimeField(input_formats=input_formats,
                                    error_messages={'invalid': errors['invalid']},
                                    localize=localize), )
        super(TimeRangeField, self).__init__(fields_, *args, **kwargs)

    def compress(self, data_list):
        return data_list


class DateTimeRangeField(fields.MultiValueField):
    u"""
    Поле с 3-мя виджетами:
    - Дата
    - Время от
    - Время до
    Для обозначения периода времени внутри одного дня
    """
    widget = widgets_custom.DateTimeRangeWidget
    hidden_widget = widgets_custom.DateTimeRangeHiddenWidget
    default_error_messages = {'invalid': u'Format error',
                              'invalid_order': u'Invalid order',
                              'not_all_filled': u'Not all filled'}

    def __init__(self, *args, **kwargs):
        errors = self.default_error_messages.copy()
        if 'error_messages' in kwargs:
            errors.update(kwargs['error_messages'])

        localize = kwargs.get('localize', False)

        fields_ = (fields.DateField(error_messages={'invalid': errors['invalid']},
                                    localize=localize),
                   fields.TimeField(error_messages={'invalid': errors['invalid']},
                                    localize=localize),
                   fields.TimeField(error_messages={'invalid': errors['invalid']},
                                    localize=localize), )
        super(DateTimeRangeField, self).__init__(fields_, *args, **kwargs)

    def validate(self, value):
        find_none = False
        find_filled = False
        for i in range(3):
            if value[i]:
                find_filled = True
            else:
                find_none = True

        if find_none and find_filled:
            raise ValidationError(self.default_error_messages['not_all_filled'])

        if find_filled and value[1] > value[2]:
            raise ValidationError(self.default_error_messages['invalid_order'])

    def compress(self, data_list):
        return data_list


class FormsetField(fields.Field):
    u''' Таблица со списком форм '''

    default_error_messages = {
        'invalid': _('Invalid Formset'),
    }

    def __init__(self, formset_class, layout, template, template_context, *vargs, **kwargs):
        self._formset_class = formset_class
        self._layout = layout
        self._template_context = template_context
        self._initial = None
        self._template = template if template else 'lib/forms/formset.html'
        super(FormsetField, self).__init__(*vargs, **kwargs)

    def validate(self, value):
        if not value.is_valid():
            raise ValidationError(self.error_messages['invalid'])

    def clean(self, value):
        formset = super(FormsetField, self).clean(value)
        return formset.cleaned_data

    def widget_attrs(self, widget):
        return {
            'formset_class': self._formset_class,
            'template': self._template,
            'template_context': self._template_context,
        }

    def _has_changed(self, initial, data):
        if data.is_valid():
            diff = formset_field_diff(data=data.cleaned_data, initial=initial)
            return bool(diff)
        return True

    @property
    def layout(self):
        return self._layout

    @staticmethod
    def remove_empty(data):
        u"""
        Форматирует список строк, вычищая из него:
        - Удаленные строки
        - Пустые строки (которые для extra)
        """
        if not data:
            return []

        res = []
        for row in data:
            if row and not row.get(u'DELETE'):
                res.append(row)
        return res
