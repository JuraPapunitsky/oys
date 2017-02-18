# coding=utf-8
import re
from dateutil.relativedelta import relativedelta
from django import forms
from django.utils.datetime_safe import datetime
from django.utils.translation import ugettext_lazy as _

from . import models

hidden_field = forms.CharField(max_length=250, widget=forms.HiddenInput)



# Общие поля договоров страхования
GENERAL_FIELDS = [
    'step', 'substep', 'layer', 'main_product', 'main_product_text', 'd_start', 'term_insurance',
    'ins_person_pin', 'ins_person_lname', 'ins_person_fname', 'ins_person_mname', 'ins_person_gender',
    'ins_person_birthday', 'ins_country', 'ins_city', 'ins_city_custom', 'ins_address', 'ins_index',
    'ins_street', 'ins_house', 'ins_apartment', 'ins_phone', 'ins_email', 'delivery_type',
    'delivery_date', 'delivery_time', 'delivery_city', 'delivery_region', 'delivery_street',
    'delivery_house', 'delivery_apartment', 'delivery_phone', 'delivery_comment', 'delivery_takeout',
    'delivery_email', 'payment_type', 's_premium',
]

VEHICLE_FIELDS = [
    'p2_selected', 'p11_selected', 'p12_selected', 'auto_type', 'auto_mark', 'auto_model',
    'auto_engine_capacity', 'auto_payload', 'cnt_seats', 'auto_createyear', 'auto_vin', 'auto_engine',
    'auto_chassis', 'auto_number', 'auto_region', 'auto_cost', 'p2_inscompany', 'p11_inscompany',
    'p11_product_option', 'p11_beneficiary', 'p11_bank_beneficiary', 'p12_inscompany', 'p12_beneficiary',
    'p12_bank_beneficiary', 'insurance_coverage', 'accidents_quantity', 'evacuation', 'cvi_extension_sum',
    'accident_ins_sum', 'accident_ins_drivers', 'additional_drivers', 'additional_driver_2', 'ins_owner',
    'owner_pin', 'owner_lname', 'owner_fname', 'owner_mname', 'owner_gender', 'owner_birthday', 'owner_country',
    'owner_city', 'owner_city_custom', 'owner_address', 'owner_index', 'owner_street', 'owner_house',
    'owner_apartment', 'owner_phone', 'owner_email', 'ad1_pin', 'ad1_lname', 'ad1_fname', 'ad1_mname',
    'ad1_gender', 'ad1_birthday', 'ad1_country', 'ad1_city', 'ad1_city_custom', 'ad1_address', 'ad1_index',
    'ad1_street', 'ad1_house', 'ad1_apartment', 'ad1_phone', 'ad1_email', 'ad2_pin', 'ad2_lname', 'ad2_fname',
    'ad2_mname', 'ad2_gender', 'ad2_birthday', 'ad2_country', 'ad2_city', 'ad2_city_custom', 'ad2_address',
    'ad2_index', 'ad2_street', 'ad2_house', 'ad2_apartment', 'ad2_phone', 'ad2_email', 'ateshgah_beshlik',
    'ateshgah_icbariplus', 'ateshgah_superkasko'
]

PROPERTY_FIELDS = [
    'p3_selected', 'realty_type', 'city', 'branch', 's_insurance', 'franchise', 'p3_inscompany',
    'n_reestr', 'document_reason', 'address', 'index', 'using_method'
]

TRAVEL_FIELDS = [
    'p4_selected', 'p4_inscompany', 'currency', 'rest_type', 'countries', 'ins_value',
    'risk_group', 'd_start', 'd_end', 'insured_days', 'traveller_first_name', 'traveller_last_name',
    'traveller_middle_name', 'traveller_n_passport', 'traveller_birthday', 'traveller_gender', 'traveller_address',
    'traveller_pin', 'traveller_city', 'embassy', 'country_of_departure', 'departure_type', 'rest_type_extended', 'rest_term_year'
]

HEALTH_FIELDS = [
    'p9_1_selected', 'p9_2_selected', 'p9_3_selected', 'p9_inscompany', 'deductible', 'vac', 'massage',
    'refund_vip', 'program69_extended', 'insured_lname', 'insured_fname', 'insured_mname', 'insured_birthday',
    'p9_1_payment', 'p9_2_payment', 'p9_3_payment'
]


class VehicleContract(forms.ModelForm):
    """
    Форма договора на страхование ТС
    """

    class Meta:
        model = models.VehicleContract
        fields = GENERAL_FIELDS + VEHICLE_FIELDS

    def clean(self):
        cleaned_data = super(VehicleContract, self).clean()

        # Дополнительная валидация данных
        birthday_fields = ['ins_person_birthday', ]  # поля с датами рождения водителей, страхователей и т.д., старше 18
        required_fields = ['ins_person_pin', 'ins_person_lname', 'ins_person_fname', 'ins_person_mname',
                           'ins_person_gender', 'ins_person_birthday', 'ins_country', 'ins_index', 'ins_phone',
                           'delivery_type', 'd_start', 'term_insurance']  # список обязательных полей

        # Валидация дополнительных данных о ТС
        vin = cleaned_data.get('auto_vin')
        engine = cleaned_data.get('auto_engine')
        chassis = cleaned_data.get('auto_chassis')
        if not(vin or engine or chassis):
            msg = _(u'Требуется заполнить VIN, Номер двигателя или Номер кузова')
            self.add_error('auto_vin', msg)
            self.add_error('auto_engine', msg)
            self.add_error('auto_chassis', msg)
        else:
            pass

        # Валидация данных о страхователе (для Азербайджана валидируется полный адрес,
        # а для других стран - кастомный город и адрес)
        country = cleaned_data.get('ins_country')
        if country == 4:
            required_fields.extend(('ins_city', 'ins_street', 'ins_house'))
        else:
            required_fields.extend(('ins_city_custom', 'ins_address'))

        # Валидация для Уверенный водитель
        if cleaned_data.get('p11_selected'):

            if cleaned_data.get('p11_beneficiary') == 'bank' and not cleaned_data.get('p11_bank_beneficiary'):
                required_fields.append('p11_bank_beneficiary')

        # Валидация для Простое КАСКО
        if cleaned_data.get('p12_selected'):

            # Валидация банка выгодопреобретателя (обязательное)
            if cleaned_data.get('p12_beneficiary') == 'bank' and not cleaned_data.get('p12_bank_beneficiary'):
                required_fields.append('p12_bank_beneficiary')

            # Если водитель и владелец разные (не установлен признак)
            if not cleaned_data.get('ins_owner', True):
                required_fields.extend(('owner_fname', 'owner_lname', 'owner_mname', 'owner_gender', 'owner_birthday',
                                        'owner_pin', 'owner_country', 'owner_index', 'owner_phone'))
                country = cleaned_data.get('owner_country')
                if country == 4:
                    required_fields.extend(('owner_city', 'owner_street', 'owner_house'))
                else:
                    required_fields.extend(('owner_city_custom', 'owner_address'))
                birthday_fields.append('owner_birthday')

            # Если указаны дополнительные водители
            has_add_drivers = cleaned_data.get('additional_drivers', False)
            if has_add_drivers:
                required_fields.extend(('ad1_fname', 'ad1_lname', 'ad1_mname', 'ad1_gender', 'ad1_birthday', 'ad1_pin',
                                        'ad1_country', 'ad1_index', 'ad1_phone'))
                country = cleaned_data.get('ad1_country')
                if country == 4:
                    required_fields.extend(('ad1_city', 'ad1_street', 'ad1_house'))
                else:
                    required_fields.extend(('ad1_city_custom', 'ad1_address'))
                birthday_fields.append('ad1_birthday')

            # Второй дополнительный водитель
            has_add_driver2 = cleaned_data.get('additional_driver_2', False)
            if has_add_drivers and has_add_driver2:
                required_fields.extend(('ad2_fname', 'ad2_lname', 'ad2_mname', 'ad2_gender', 'ad2_birthday', 'ad2_pin',
                                        'ad2_country', 'ad2_index', 'ad2_phone'))
                country = cleaned_data.get('ad2_country')
                if country == 4:
                    required_fields.extend(('ad2_city', 'ad2_street', 'ad2_house'))
                else:
                    required_fields.extend(('ad2_city_custom', 'ad2_address'))
                birthday_fields.append('ad2_birthday')

        # Валидация обязательности заполнения полей доставки
        delivery = cleaned_data.get('delivery_type')
        if delivery == 'courier':
            required_fields.extend(('delivery_date', 'delivery_time', 'delivery_street', 'delivery_city',
                                    'delivery_house', 'delivery_phone'))
        elif delivery == 'takeout':
            required_fields.extend(('delivery_takeout', ))
        elif delivery == 'email':
            required_fields.extend(('delivery_email', ))

        for f in required_fields:
            if not cleaned_data.get(f):
                self.add_error(f, _('This field is required.'))

        # Логическая валидация значений

        # Возраст более 18 лет
        for f in birthday_fields:
            if (f not in self.errors) and (cleaned_data.get(f) + relativedelta(years=18) >= datetime.now().date()):
                self.add_error(f, _('Age must exceed 18 full years.'))

        # Дата позже сегодняшнего дня
        next_day_fields = ('d_start', 'delivery_date')
        for f in next_day_fields:
            if cleaned_data.get(f) and \
                    (f not in self.errors) and \
                    (cleaned_data.get(f) - relativedelta(days=1) < datetime.now().date()):
                self.add_error(f, _('This date must be tomorrow or afterward.'))

        # Регион доставки
        delivery_city = cleaned_data.get('delivery_city')
        delivery_region = cleaned_data.get('delivery_region')
        if delivery_city == 1 and not delivery_region:
            self.add_error('delivery_region', _('This field is required.'))


class PropertyContract(forms.ModelForm):
    """
    Форма договора на страхование ТС
    """

    class Meta:
        model = models.PropertyContract
        fields = GENERAL_FIELDS + PROPERTY_FIELDS

    def clean(self):
        cleaned_data = super(PropertyContract, self).clean()

        # Дополнительная валидация данных
        birthday_fields = ['ins_person_birthday', ]  # поля с датами рождения водителей, страхователей и т.д., старше 18
        required_fields = ['ins_person_pin', 'ins_person_lname', 'ins_person_fname', 'ins_person_mname',
                           'ins_person_gender', 'ins_person_birthday', 'ins_country', 'ins_index', 'ins_phone',
                           'delivery_type', 'd_start', 'term_insurance']  # список обязательных полей

        # Валидация дополнительных данных о недвижимости
        n_reestr = cleaned_data.get('n_reestr')
        document_reason = cleaned_data.get('document_reason')
        if not(n_reestr or document_reason):
            msg = _(u'Требуется заполнить Номер из госреестра или Номер другого документа')
            self.add_error('n_reestr', msg)
            self.add_error('document_reason', msg)
        else:
            pass

        required_fields.extend(('address', 'index'))
        if cleaned_data.get('realty_type') != 1:
            required_fields.append('using_method')

        # Валидация данных о страхователе (для Азербайджана валидируется полный адрес,
        # а для других стран - кастомный город и адрес)
        country = cleaned_data.get('ins_country')
        if country == 4:
            required_fields.extend(('ins_city', 'ins_street', 'ins_house'))
        else:
            required_fields.extend(('ins_city_custom', 'ins_address'))

        # Валидация обязательности заполнения полей доставки
        delivery = cleaned_data.get('delivery_type')
        if delivery == 'courier':
            required_fields.extend(('delivery_date', 'delivery_time', 'delivery_street', 'delivery_city',
                                    'delivery_house', 'delivery_phone'))
        elif delivery == 'takeout':
            required_fields.extend(('delivery_takeout', ))
        elif delivery == 'email':
            required_fields.extend(('delivery_email', ))

        for f in required_fields:
            if not cleaned_data.get(f):
                self.add_error(f, _('This field is required.'))

        # Логическая валидация значений

        # Возраст более 18 лет
        for f in birthday_fields:
            if (f not in self.errors) and (cleaned_data.get(f) + relativedelta(years=18) >= datetime.now().date()):
                self.add_error(f, _('Age must exceed 18 full years.'))

        # Дата позже сегодняшнего дня
        next_day_fields = ('d_start', 'delivery_date')
        for f in next_day_fields:
            if cleaned_data.get(f) and \
                    (f not in self.errors) and \
                    (cleaned_data.get(f) - relativedelta(days=1) < datetime.now().date()):
                self.add_error(f, _('This date must be tomorrow or afterward.'))

        # Валидация поля Номер в реестре
        n_reestr = cleaned_data.get('n_reestr')
        if n_reestr:
            if not re.match(u'[A-Za-züöğçşəıƏÜĞÇŞÖİI]{2}\d{7,}', n_reestr, re.UNICODE):
                self.add_error('n_reestr', _(u'2 буквы, 7 и более цифр, например ÖM1567356'))

        # Регион доставки
        delivery_city = cleaned_data.get('delivery_city')
        delivery_region = cleaned_data.get('delivery_region')
        if delivery_city == 1 and not delivery_region:
            self.add_error('delivery_region', _('This field is required.'))


class PropertyContractSave(forms.ModelForm):
    """
    Форма договора на страхование ТС
    """

    class Meta:
        model = models.PropertyContract
        fields = GENERAL_FIELDS + PROPERTY_FIELDS


class TravelContract(forms.ModelForm):
    u"""
    Форма договора ВЗР
    """
    class Meta:
        model = models.TravelContract
        fields = GENERAL_FIELDS + TRAVEL_FIELDS

    def clean(self):
        cleaned_data = super(TravelContract, self).clean()
        # Дополнительная валидация данных
        birthday_fields = ['ins_person_birthday']  # поля с датами рождения водителей, страхователей и т.д., старше 18
        required_fields = ['ins_person_pin', 'ins_person_lname', 'ins_person_fname', 'ins_person_mname',
                           'ins_person_gender', 'ins_person_birthday', 'ins_country', 'ins_index', 'ins_phone',
                           'delivery_type', 'd_start', 'd_end', 'insured_days', 'rest_type', 'embassy',
                           'traveller_first_name', 'traveller_middle_name', 'traveller_last_name',
                           'traveller_n_passport', 'traveller_birthday', 'traveller_gender']  # список обязательных полей

        # Валидация обязательности заполнения полей доставки
        delivery = cleaned_data.get('delivery_type')
        if delivery == 'courier':
            required_fields.extend(('delivery_date', 'delivery_time', 'delivery_street', 'delivery_city',
                                    'delivery_house', 'delivery_phone'))
        elif delivery == 'takeout':
            required_fields.extend(('delivery_takeout', ))

        elif delivery == 'email':
            required_fields.extend(('delivery_email', ))

        # Валидация для ФИО застрахованного из загранника. Поля обязательны только для Атешгях
        ins_company = cleaned_data.get('p4_inscompany')
        if ins_company == 11:
            required_fields.extend(['traveller_address', 'traveller_city', 'traveller_pin'])

        for f in required_fields:
            if not cleaned_data.get(f):
                self.add_error(f, _('This field is required.'))

        # Полис максимум на 1 год
        d_start = cleaned_data.get('d_start')
        d_end = cleaned_data.get('d_end')
        if d_start > d_end:
            self.add_error('d_end', _(u'Должно быть больше даты начала действия договора'))

        print d_start + relativedelta(years=1) - relativedelta(days=1), d_end
        if d_start + relativedelta(years=1) - relativedelta(days=1) < d_end:
            self.add_error('d_end', _(u'Максимальный срок действия полиса - 1 год'))

        # Возраст более 18 лет
        for f in birthday_fields:
            if (f not in self.errors) and (cleaned_data.get(f) + relativedelta(years=18) >= datetime.now().date()):
                self.add_error(f, _('Age must exceed 18 full years.'))

        # Дата позже сегодняшнего дня
        next_day_fields = ('delivery_date', 'd_start', 'd_end')
        for f in next_day_fields:
            if cleaned_data.get(f) and \
                    (f not in self.errors) and \
                    (cleaned_data.get(f) - relativedelta(days=1) < datetime.now().date()):
                self.add_error(f, _('This date must be tomorrow or afterward.'))

        # Регион доставки
        delivery_city = cleaned_data.get('delivery_city')
        delivery_region = cleaned_data.get('delivery_region')
        if delivery_city == 1 and not delivery_region:
            self.add_error('delivery_region', _('This field is required.'))


class HealthContract(forms.ModelForm):
    u"""
    Форма договора ВЗР
    """
    class Meta:
        model = models.HealthContract
        fields = GENERAL_FIELDS + HEALTH_FIELDS

    def clean(self):
        cleaned_data = super(HealthContract, self).clean()
        # Дополнительная валидация данных
        birthday_fields = ['ins_person_birthday', ]  # поля с датами рождения водителей, страхователей и т.д., старше 18
        required_fields = ['ins_person_pin', 'ins_person_lname', 'ins_person_fname', 'ins_person_mname',
                           'ins_person_gender', 'ins_person_birthday', 'ins_country', 'ins_index', 'ins_phone',
                           'delivery_type', 'insured_birthday', 'insured_fname', 'insured_lname', 'insured_mname']

        # Валидация обязательности заполнения полей доставки
        delivery = cleaned_data.get('delivery_type')
        if delivery == 'courier':
            required_fields.extend(('delivery_date', 'delivery_time', 'delivery_street', 'delivery_city',
                                    'delivery_house', 'delivery_phone'))
        elif delivery == 'takeout':
            required_fields.extend(('delivery_takeout', ))

        elif delivery == 'email':
            required_fields.extend(('delivery_email', ))

        for f in required_fields:
            if not cleaned_data.get(f):
                self.add_error(f, _('This field is required.'))

        if ('insured_birthday' not in self.errors) and cleaned_data.get('insured_birthday') > datetime.now().date():
            self.add_error('insured_birthday', _('Insured birthday must be today or earlier'))

        # Возраст более 18 лет
        for f in birthday_fields:
            if (f not in self.errors) and (cleaned_data.get(f) + relativedelta(years=18) >= datetime.now().date()):
                self.add_error(f, _('Age must exceed 18 full years.'))

        # Дата позже сегодняшнего дня
        next_day_fields = ('delivery_date', 'd_start')
        for f in next_day_fields:
            if cleaned_data.get(f) and \
                    (f not in self.errors) and \
                    (cleaned_data.get(f) - relativedelta(days=1) < datetime.now().date()):
                self.add_error(f, _('This date must be tomorrow or afterward.'))

        # Регион доставки
        delivery_city = cleaned_data.get('delivery_city')
        delivery_region = cleaned_data.get('delivery_region')
        if delivery_city == 1 and not delivery_region:
            self.add_error('delivery_region', _('This field is required.'))


class OnlinePaymentForm(forms.Form):
    AMOUNT = hidden_field
    ORDER = hidden_field
    CURRENCY = hidden_field
    DESC = hidden_field
    MERCH_NAME = hidden_field
    MERCH_URL = hidden_field
    TERMINAL = hidden_field
    EMAIL = hidden_field
    TRTYPE = hidden_field
    COUNTRY = hidden_field
    MERCH_GMT = hidden_field
    TIMESTAMP = hidden_field
    NONCE = hidden_field
    BACKREF = hidden_field
    P_SIGN = hidden_field
