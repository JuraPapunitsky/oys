from django.shortcuts import render, render_to_response
from sale.models import TransportType, EngineCapacity, PassengerSeats, \
    BearingCapacity, PersonType, CarManufacturer, DocType


def auto_step_1(request):
    transport_types = TransportType.objects.all()
    engine_capacitys = EngineCapacity.objects.all()
    passenger_seats = PassengerSeats.objects.all()
    bearing_capasitys = BearingCapacity.objects.all()
    person_types = PersonType.objects.all()
    doc_types = DocType.objects.all()
    js = '';
    for transport_type in transport_types:
        if transport_type.description == 'engine':
            js = js + str(transport_type.id) + ': {'
            for engine_capacity in engine_capacitys:
                js = js + str(engine_capacity.id) + ': {'
                for person_type in person_types:
                    js = js + str(person_type.id) + ': {'
                    for doc_type in doc_types:
                        js = js + str(doc_type.id) + ': '+ str(transport_type.premium+engine_capacity.premium+person_type.premium+doc_type.premium)+', '
                    js = js+'},'
                js = js + '},'
            js = js + '},'
        if transport_type.description == 'none':
            js = js + str(transport_type.id) + ': {'
            for person_type in person_types:
                js = js + str(person_type.id) + ': {'
                for doc_type in doc_types:
                    js = js + str(doc_type.id) + ': ' + str(transport_type.premium + person_type.premium + doc_type.premium) + ','
                js = js + '},'
            js = js + '},'
        if transport_type.description == 'seats':
            js = js + str(transport_type.id) + ': {'
            for passenger_seat in passenger_seats:
                js = js + str(passenger_seat.id) + ': {'
                for person_type in person_types:
                    js = js + str(person_type.id) + ': {'
                    for doc_type in doc_types:
                        js = js + str(doc_type.id) + ': '+ str(transport_type.premium+passenger_seat.premium+person_type.premium+doc_type.premium)+', '
                    js = js+'},'
                js = js + '},'
            js = js + '},'
        if transport_type.description == 'capacity':
            js = js + str(transport_type.id) + ': {'
            for bearing_capasity in bearing_capasitys:
                js = js + str(bearing_capasity.id) + ': {'
                for person_type in person_types:
                    js = js + str(person_type.id) + ': {'
                    for doc_type in doc_types:
                        js = js + str(doc_type.id) + ': '+ str(transport_type.premium+bearing_capasity.premium+person_type.premium+doc_type.premium)+', '
                    js = js+'},'
                js = js + '},'
            js = js + '},'

    return render_to_response('sale/auto/sale-step-1.html', {
        'transport_types': transport_types,
        'engine_capacitys': engine_capacitys,
        'passenger_seats': passenger_seats,
        'bearing_capasitys': bearing_capasitys,
        'person_types': person_types,
        'doc_types': doc_types,
        'js': js,

    })


def auto_step_2(request):

    return render_to_response('sale/auto/sale-step-2.html', {
        'car_manufacturers': CarManufacturer.objects.all(),
    })


def auto_step_3(request):
    return render_to_response('sale/auto/sale-step-3.html')