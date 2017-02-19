from django.shortcuts import render, render_to_response, redirect
from datetime import datetime
from sale.models import TransportType, EngineCapacity, PassengerSeats, \
    BearingCapacity, PersonType, CarManufacturer, DocType, CarModel, CarTypeCarModel, \
    ClientData, Territory


def auto_step_1(request):
    transport_types = TransportType.objects.all()
    engine_capacitys = EngineCapacity.objects.all()
    passenger_seats = PassengerSeats.objects.all()
    bearing_capasitys = BearingCapacity.objects.all()
    person_types = PersonType.objects.all()
    doc_types = DocType.objects.all()
    js = '';
    for transport_type in transport_types:
        if transport_type.description == '#carEngine':
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
        if transport_type.description == '#carSize':
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
        if transport_type.description == '#carWeight':
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

    transport_types = TransportType.objects.all()
    person_types = PersonType.objects.all()
    territorys = Territory.objects.all()
    car_manufacturers = CarManufacturer.objects.all()


    js = '';
    transport_selected = 1;
    percon_selected = 1;
    if request.POST:
        transport_selected = request.POST.get('car[type]')
        percon_selected = int(request.POST.get('person'))

    for car_manufacturer in car_manufacturers:
        js = js + str(car_manufacturer.id) + ': {'
        car_models = CarModel.objects.all().filter(brand=car_manufacturer.id)
        for car_model in car_models:
            js = js + str(car_model.id) + ': { title: ' + '"' + str(car_model.model)+'"' + ', type: {'
            car_type_car_models = CarTypeCarModel.objects.all().filter(car_model=car_model)
            for car_type_car_model in car_type_car_models:
                js = js + str(car_type_car_model.transport_type.id) + ': "' + str(car_type_car_model.transport_type.transport_type.encode('utf-8').strip()) + '",'
            js = js + '},'
            js = js +' more: {'
            for car_type_car_model in car_type_car_models:
                js = js + str(car_type_car_model.transport_type.id) + ': "' + str(car_type_car_model.transport_type.description) + '",'
            js = js + '},},'
        js = js + '},'

    return render_to_response('sale/auto/sale-step-2.html', {
        'car_manufacturers': car_manufacturers,
        'person_types': person_types,
        'transport_types': transport_types,
        'transport_selected': transport_selected,
        'person_selected': percon_selected,
        'territoryes': territorys,
        'js': js,
    })


def auto_step_3(request):
    if request.POST:
        car_engine = str(request.POST.get('car[engine]'))
        car_size = str(request.POST.get('car[size]'))
        car_weight = str(request.POST.get('car[weight]'))
        type = ''
        value = ''
        param = ''
        if car_engine == '' and car_size == '':
            car_engine = 0
            car_size = 0

            type = 'Max weight',
            value = car_engine

        elif car_size == '' and car_weight == '':
            car_size = 0
            car_weight = 0

            type = 'Capacity engine',
            value = car_engine

        elif car_weight == '' and car_engine == '':
            car_weight = 0
            car_engine = 0

            type = 'Seats',
            value = car_size

        client_data = ClientData(
            registration_number= request.POST.get('car[num]'),
            car_manufacturer= CarManufacturer.objects.get(id=request.POST.get('car[make]')),
            car_model= CarModel.objects.get(id=request.POST.get('car[model]')),
            car_type= TransportType.objects.get(id=request.POST.get('car[type]')),
            car_engine= float(car_engine),
            car_size= float(car_size),
            car_weight= float(car_weight),
            person_type=PersonType.objects.get(id=request.POST.get('person[type]')),
            pin_code= request.POST.get('person[id]'),
            driver_license_series= request.POST.get('person[serie]'),
            driver_license_number= request.POST.get('person[num]'),
            start_date= datetime.strptime(str(request.POST.get('start')), '%d.%m.%Y'),
            territory= Territory.objects.get(id=request.POST.get('territory')),
            phone= request.POST.get('tel'),
            email= request.POST.get('email'),
        )
        client_data.save()
        return render_to_response('sale/auto/sale-step-3.html', {
            'client_data': client_data,
            'type': type,
            'value': value,
        })
    else:
        return redirect('/sale/auto-step-3/')

