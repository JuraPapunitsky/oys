# coding=utf-8
import random
from django import template
from django.utils.translation import ugettext as _

register = template.Library()

@register.assignment_tag
def get_random_background():
    backgrounds = (
        {
            'background_url': 'common/img/back1.jpg',
            'text': _(u'Есть вещи, о которых стоит позаботиться заранее!')
        },
        {
            'background_url': 'common/img/back2.jpg',
            'text': _(u'Нам доверяют самое ценное!')
        },
        {
            'background_url': 'common/img/back4.jpg',
            'text': _(u'Защитите самое дорогое. Финансовая поддержка в трудных жизненных ситуациях!')
        },
        {
            'background_url': 'common/img/back5.jpg',
            'text': _(u'Позаботьтесь о своих любимых вместе с нами!')
        },
        {
            'background_url': 'common/img/back6.jpg',
            'text': _(u'Смело отправляйтесь<br/>на встречу ярким впечатлениям!')
        },
        {
            'background_url': 'common/img/back7.jpg',
            'text': _(u'Пусть ваш отдых пройдет легко и весело!')
        },
        {
            'background_url': 'common/img/back8.jpg',
            'text': _(u'Смело отправляйтесь<br/>на встречу ярким впечатлениям!')
        },
        {
            'background_url': 'common/img/back9.jpg',
            'text': _(u'Водить ты можешь не уметь, но застрахован быть обязан!')
        },
        {
            'background_url': 'common/img/back10.jpg',
            'text': _(u'Водить ты можешь не уметь, но застрахован быть обязан!')
        },
    )
    random.seed()
    return random.choice(backgrounds)

