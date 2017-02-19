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
    premium = models.FloatField(10)

    def get_premium(self):
        self.premium = self.car_type + self.get_engine_premium(self);

    def get_engine_premium(self):
        if self.car_engine == 0:
            return 0
        start_capacity = 1500
        for engine_capasity in EngineCapacity.objects.all():
            if self.car_engine <= start_capacity:
                return engine_capasity.premium
            if start_capacity > 5000:
                return engine_capasity.premium
            else:
                start_capacity = start_capacity + 500


    def get_size_premium(self):
        if self.car_size == 0:
            return 0

    def get_weight_premium(self):
        if self.car_weight == 0:
            return 0
