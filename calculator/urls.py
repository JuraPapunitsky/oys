# coding=utf-8
from django.conf.urls import patterns, url
from .views import ajax_calculator_reset, VehicleProductCalculator, PropertyProductCalculator, TravelProductCalculator, \
    HealthProductCalculator, OnlinePaymentFormView, check_payment



urlpatterns = patterns(
    '',
    url(r'^modal/$', view=ajax_calculator_reset, name='general_product_calculator'),
    url(r'^modal/vehicle/$', view=VehicleProductCalculator.as_view(), name='vehicle_product_calculator'),
    url(r'^modal/property/$', view=PropertyProductCalculator.as_view(), name='property_product_calculator'),
    url(r'^modal/travel/$', view=TravelProductCalculator.as_view(), name='travel_product_calculator'),
    url(r'^modal/health/$', view=HealthProductCalculator.as_view(), name='health_product_calculator'),

    # online-оплата
    url(r'^online_payment_form/$', view=OnlinePaymentFormView.as_view(), name='online_payment_form'),
    url(r'^check_payment/(?P<product>(vehicle))/(?P<key>[0-9A-Za-z-]{36})/$', view=check_payment, name='check_payment'),
)
