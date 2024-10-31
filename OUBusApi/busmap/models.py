from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatar/%Y/%m/')
    def __str__(self):
        return self.username

class BaseModel(models.Model):
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True

class BankAccount(models.Model):
    accountNumber = models.CharField(max_length=255)
    accountName = models.CharField(max_length=255)
    bankName = models.CharField(max_length=255)
    def __str__(self):
        return self.accountNumber

class Driver(User):
    bankAccount = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    def __str__(self):
        return self.username

class Client(User):
    registry_trip = models.ManyToManyField('VehicalRoute', related_name="VehicalRoutes", through='RegisterTrip')
    balance = models.FloatField(default=0)
    
    def __str__(self):
        return self.username

class Vehicle(models.Model):  # Thay đổi từ class Vehical()
    seat_number = models.IntegerField()
    plate_number = models.CharField(max_length=255)
    driver = models.ForeignKey(Driver, on_delete=models.PROTECT)
    # def __str__(self):
    #     return self.plate_number


class Bus(Vehicle):  # Thay đổi từ class Bus(Vehical)
    pass

class Location(models.Model):  # Thay đổi từ class Location()
    imei = models.CharField(max_length=20)
    latitude = models.FloatField()
    longitude = models.FloatField()
    name_location = models.CharField(max_length=255)
    def __str__(self):
        return self.name_location


class Station(models.Model):  # Thay đổi từ class Station()
    name = models.CharField(max_length=255)
    location = models.ForeignKey(Location, null=True, on_delete=models.PROTECT)
    def __str__(self):
        return self.name


class Route(models.Model):  # Thay đổi từ class Route()
    stop_station = models.ManyToManyField(Station, related_name="routes")
    start_point = models.ForeignKey(Station, related_name="start_point", on_delete=models.PROTECT)
    end_point = models.ForeignKey(Station, related_name="end_point", on_delete=models.PROTECT)
    def __str__(self):
        return f"{self.start_point} to {self.end_point}"

class VehicalRoute(models.Model):
    route = models.ForeignKey(Route, on_delete=models.PROTECT)
    vehical = models.ForeignKey(Vehicle, on_delete=models.PROTECT)  # Thay đổi từ Vehical
    driver = models.ForeignKey(Driver, on_delete=models.PROTECT)
    state = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    date_operation = models.DateTimeField()
    class Meta:
        unique_together = ('route', 'vehical','driver')

class RegisterTrip(BaseModel):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    vehical_route = models.ForeignKey(VehicalRoute, on_delete=models.CASCADE)
    is_pay = models.BooleanField(default=True)
    time_outbound = models.DateTimeField()
    time_return = models.DateTimeField()

    class Meta:
        unique_together = ('client', 'vehical_route')  # Đảm bảo đúng tên trường

class VehicleTicket(BaseModel):
    register_trip = models.ForeignKey(RegisterTrip, on_delete=models.CASCADE)
    vehical_route = models.ForeignKey(VehicalRoute, on_delete=models.CASCADE)
    time_outbound = models.DateTimeField()
    time_return = models.DateTimeField()
    is_pay = models.BooleanField(default=False)

    class Meta:
        unique_together = ('register_trip', 'vehical_route')
