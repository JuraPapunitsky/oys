from django.db import models


class TransportType(models.Model):
    transport_type = models.CharField(max_length=200)
    premium = models.FloatField(max_length=10)
    description = models.CharField(max_length=255)

    def __str__(self):
        return str(self.id)


class EngineCapacity(models.Model):
    engine_capacity = models.CharField(max_length=200)
    premium = models.FloatField(max_length=10)
    tag_value = models.IntegerField()


class PassengerSeats(models.Model):
    passenger_seats = models.CharField(max_length=200)
    premium = models.FloatField(max_length=10)
    tag_value = models.IntegerField()


class BearingCapacity(models.Model):
    bearing_capacity = models.CharField(max_length=200)
    premium = models.FloatField(max_length=10)
    tag_value = models.IntegerField()


class PersonType(models.Model):
    person_type = models.CharField(max_length=200)
    premium = models.FloatField(max_length=10)
    tag_value = models.IntegerField()


class DocType(models.Model):
    doc_type = models.CharField(max_length=200)
    premium = models.FloatField(max_length=10)


class CarManufacturer(models.Model):
    name = models.CharField(max_length=200)
    tag_value = models.IntegerField()

    def __str__(self):
        return  self.name


class CarModel(models.Model):
    brand = models.ForeignKey(CarManufacturer)
    model = models.CharField(max_length=200)

    def __str__(self):
        return self.model


class CarTypeCarModel(models.Model):
    transport_type = models.ForeignKey(TransportType)
    car_model = models.ForeignKey(CarModel)


class Territory(models.Model):
    name = models.CharField(max_length=200)
    tag_value = models.IntegerField()


class ClientData(models.Model):
    registration_number = models.CharField(max_length=200)
    car_manufacturer = models.ForeignKey(CarManufacturer)
    car_model = models.ForeignKey(CarModel)
    car_type = models.ForeignKey(TransportType)
    car_engine = models.FloatField(max_length=20)
    car_size = models.FloatField(max_length=200)
    car_weight = models.FloatField(max_length=20)
    person_type = models.ForeignKey(PersonType)
    pin_code = models.CharField(max_length=20)
    driver_license_series = models.CharField(max_length=20)
    driver_license_number = models.CharField(max_length=20)
    start_date = models.DateField()
    territory = models.ForeignKey(Territory)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    prem = models.FloatField(10)

    def set_premium(self):
        self.prem = self.car_type.premium + self.get_engine_premium() + self.get_size_premium() + self.get_weight_premium();

    def get_engine_premium(self):
        if self.car_engine == 0:
            return 0

        for engine_capasity in EngineCapacity.objects.all():
            if float(self.car_engine) <= engine_capasity.tag_value:
                return engine_capasity.premium
            elif float(self.car_engine) > 5000 and engine_capasity.tag_value == 1:
                return engine_capasity.premium

    def get_size_premium(self):
        if self.car_size == 0:
            return 0
        for passangers_seats in PassengerSeats.objects.all():
            if self.car_size <= passangers_seats.tag_value:
                return passangers_seats.premium
            elif passangers_seats.tag_value == 1:
                return passangers_seats.premium

    def get_weight_premium(self):
        if self.car_weight == 0:
            return 0
        for bearing_capacity in BearingCapacity.objects.all():
            if self.car_weight <= bearing_capacity.tag_value:
                return bearing_capacity.premium
            elif bearing_capacity.tag_value == 1:
                return bearing_capacity.premium
