# coding=utf-8

u"""
Кастомные виджеты для форм
"""

from datetime import datetime

from django.conf import settings
from django import forms
from django.forms import widgets as widgets_django
from django.core.exceptions import ValidationError
from django.forms import fields
from django.template.loader import render_to_string
from django.forms.widgets import Widget


class DateRangeWidget(widgets_django.MultiWidget):
    def __init__(self, attrs={}, date_format=None):
        attrs = dict(attrs, **{'class': 'date form-control'})

        widgets = (fields.DateInput(attrs=attrs),
                   fields.DateInput(attrs=attrs))

        super(DateRangeWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return value
        return [None, None]


class DateRangeHiddenWidget(DateRangeWidget):
    is_hidden = True

    def __init__(self, attrs={}, date_format=None):
        super(DateRangeHiddenWidget, self).__init__(attrs, date_format)
        for widget in self.widgets:
            widget.input_type = 'hidden'
            widget.is_hidden = True


class NumberRangeWidget(widgets_django.MultiWidget):
    def __init__(self, attrs={}):
        attrs = dict(attrs, **{'class': 'number form-control'})

        widgets = (forms.NumberInput(attrs=attrs),
                   forms.NumberInput(attrs=attrs))
        super(NumberRangeWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [str(value[0]), str(value[1])]
        return [None, None]


class NumberRangeHiddenWidget(NumberRangeWidget):
    is_hidden = True

    def __init__(self, attrs={}):
        super(NumberRangeHiddenWidget, self).__init__(attrs)
        for widget in self.widgets:
            widget.input_type = 'hidden'
            widget.is_hidden = True


class TimeRangeWidget(widgets_django.MultiWidget):
    def __init__(self, attrs={}, date_format=None):
        attrs = dict(attrs, **{'class': 'date form-control'})

        widgets = (fields.TextInput(attrs=attrs),
                   fields.TextInput(attrs=attrs))

        super(TimeRangeWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return value
        return [None, None]


class TimeRangeHiddenWidget(DateRangeWidget):
    is_hidden = True

    def __init__(self, attrs={}, date_format=None):
        super(DateRangeHiddenWidget, self).__init__(attrs, date_format)
        for widget in self.widgets:
            widget.input_type = 'hidden'
            widget.is_hidden = True


class DateTimeRangeWidget(widgets_django.MultiWidget):
    def __init__(self, attrs={}, date_format=None):
        date_attrs = dict(attrs, **{'class': 'date form-control'})
        time_attrs = dict(attrs, **{'class': 'time form-control'})

        widgets = (fields.DateInput(attrs=date_attrs),
                   fields.TextInput(attrs=time_attrs),
                   fields.TextInput(attrs=time_attrs))

        super(DateTimeRangeWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return value
        return [None, None, None]


class DateTimeRangeHiddenWidget(DateTimeRangeWidget):
    is_hidden = True

    def __init__(self, attrs={}, date_format=None):
        super(DateTimeRangeHiddenWidget, self).__init__(attrs, date_format)
        for widget in self.widgets:
            widget.input_type = 'hidden'
            widget.is_hidden = True


class SplitDateTimeWidget(forms.SplitDateTimeWidget):
    def __init__(self, attrs={}, date_format=None, time_format=None, date_class='date', time_class='time'):
        date_attrs = attrs.copy()
        date_attrs['class'] = date_class

        time_attrs = attrs.copy()
        time_attrs['class'] = time_class

        widgets = (fields.DateInput(attrs=date_attrs, format=date_format),
                   fields.TimeInput(attrs=time_attrs, format=time_format))

        forms.MultiWidget.__init__(self, widgets=widgets, attrs=attrs)

    def decompress(self, value):
        if value == '':
            return (None, None)

        elif type(value) == str:
            formats = ('%Y-%m-%d %H:%M:%S', '%Y-%m-%d', '%d.%m.%Y')
            for format in formats:
                datetime_val = None
                try:
                    datetime_val = datetime.strptime(value, format)
                    break
                except:
                    pass
            value = datetime_val

        return super(SplitDateTimeWidget, self).decompress(value)


class TreeWidget(widgets_django.Select):
    class Media:
        js = (settings.STATIC_URL + 'lib/forms/tree_widget.js',
              settings.STATIC_URL + 'lib/jstree/jstree.min.js',)
        css = {
            'all': (settings.STATIC_URL + 'lib/jstree/themes/default/style.min.css',)
        }

    def __init__(self, queryset, attrs=None):
        super(TreeWidget, self).__init__(attrs)
        self._queryset = queryset

    def render(self, name, value, attrs=None, choices=()):
        if value:
            value = self._queryset.get(id=value)

        application = self._queryset.model.__module__.split('.')[-0]
        model_name = self._queryset.model.__name__
        readonly = self.attrs.get('readonly', False)

        return render_to_string('lib/forms/tree_widget.html', {'attrs': attrs, 'value': value,
                                                               'name': name, 'application': application,
                                                               'model_name': model_name, 'readonly': readonly})


class SelectAutocomplete(widgets_django.Select):
    u'''
    Принимает путь к функции-обработчику и список полей,
    значение которых нужно также отправить обработчику.
    Динамически импортирует обработчик и запрашивает у него QuerySet,
    передавая фразу поиска
    '''

    class Media:
        js = (settings.STATIC_URL + 'lib/forms/autocomplete.js',)

    def __init__(self, handler_path='lib.widgets.select_autocomplete_handler',
                 handler_params=None, related_fields=None, attrs=None):
        u'''
        @param handler_path - Путь к функции-обработчику результата поиска
        @param handler_params - статические параметры, которые будут отправлены в обработчик
        @param related_fields - динамические параметры (собираются с других полей формы,
                         если нужно делать поиск зависимым от значений других полей формы)
        '''

        super(SelectAutocomplete, self).__init__(attrs)

        self._handler_path = handler_path
        self._related_fields = related_fields
        self._handler_params = handler_params

        if attrs and attrs.get('readonly', 'False') == 'True':
            self._readonly = True
        else:
            self._readonly = False

    def render(self, name, value, attrs=None, choices=()):

        return render_to_string('lib/forms/autocomplete.html', {
            'value': value,
            'attrs': attrs,
            'name': name,
            'readonly': self._readonly,
            'handler_path': self._handler_path,
            'related_fields': self._related_fields,
            'handler_params': self._handler_params,
        })


class SelectMultipleAutocomplete(widgets_django.SelectMultiple):

    class Media:
        js = (settings.STATIC_URL + 'lib/forms/autocomplete_multiple.js',)

    def __init__(self, handler_path='lib.widgets.select_autocomplete_handler',
                 handler_params=None, related_fields=None, attrs=None):
        super(SelectMultipleAutocomplete, self).__init__(attrs)

        self._handler_path = handler_path
        self._handler_params = handler_params
        self._related_fields = related_fields

        if attrs and attrs.get('readonly', 'False') == 'True':
            self._readonly = True
        else:
            self._readonly = False

    def render(self, name, value, attrs=None, choices=()):

        return render_to_string('lib/forms/autocomplete_multiple.html', {
            'value': value,
            'attrs': attrs,
            'name': name,
            'readonly': self._readonly,
            'handler_path': self._handler_path,
            'related_fields': self._related_fields,
            'handler_params': self._handler_params,
        })

    def value_from_datadict(self, data, files, name):
        """ replace scalar value ("1,2,3") to list ([1,2,3])"""

        data_dict = super(SelectMultipleAutocomplete, self).value_from_datadict(data, files, name)
        if len(data_dict) == 0:
            value = None
        else:
            value = data_dict[0]

        if not value:
            return None

        return value.split(",")


class FormsetWidget(Widget):
    u''' Виджет для Formset '''

    def __init__(self, *vargs, **kwargs):
        self._editable = 'readonly' not in kwargs['attrs']
        super(FormsetWidget, self).__init__(*vargs, **kwargs)

    def render(self, name, value, attrs):
        template = self.attrs['template']
        formset_class = self.attrs['formset_class']

        if type(value) == list or value is None:
            formset = formset_class(prefix=name, initial=value)
        else:
            formset = value

        try:
            ctx = {'formset': formset, 'editable': self._editable}
            ctx.update(self.attrs['template_context'])

            html = render_to_string(template, ctx)
            return html

        # Если по настройкам доступа, это поле внезапно появилось
        # в форме после отправки POST-запроса, ничего не выводим
        except ValidationError as e:
            if e.code == 'missing_management_form':
                return u'Не найдены данные поля'

            raise e

    def value_from_datadict(self, data, files, name):
        return self.attrs['formset_class'](data=data, files=files, prefix=name)
