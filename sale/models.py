from django.db import models

# Create your models here.


class TransportType(models.Model):
    transport_type = models.CharField(max_length=200)
    premium = models.FloatField(max_length=10)
    description = models.CharField(max_length=255)




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




class CarModel(models.Model):
    brand = models.ForeignKey(CarManufacturer)
    model = models.CharField(max_length=200)
    car_type = models.ForeignKey('CarType')




class CarType(models.Model):
    name = models.CharField(max_length=200)
    tag_value = models.IntegerField()



class Territory(models.Model):
    name = models.CharField(max_length=200)
    tag_value = models.IntegerField()



class ClientData(models.Model):
    registration_number = models.CharField(max_length=200)
    car_manufacturer = models.ForeignKey(CarManufacturer)
    car_model = models.ForeignKey(CarModel)
    car_type = models.ForeignKey(CarType)
    person_type = models.ForeignKey(PersonType)
    pin_code = models.CharField(max_length=20)
    driver_license_series = models.CharField(max_length=20)
    driver_license_number = models.CharField(max_length=20)
    start_date = models.DateField()
    territory = models.ForeignKey(Territory)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
