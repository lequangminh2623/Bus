from rest_framework import serializers
from .models import User, BankAccount, Driver, Client, Vehicle, Bus, Location, Station, Route, VehicalRoute, RegisterTrip, VehicleTicket

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = ['id', 'accountNumber', 'accountName', 'bankName']

class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ['id', 'username', 'email', 'avatar', 'bankAccount']

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'avatar']
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'avatar': {'required': False, 'allow_null': True}
        }

    def create(self, validated_data):
        # Create and return the Client instance without password handling
        client = Client(**validated_data)
        client.save()
        return client

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['id', 'seat_number', 'plate_number', 'driver']

class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = ['id', 'seat_number', 'plate_number', 'driver']

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'imei', 'latitude', 'longitude', 'name_location']

class StationSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    class Meta:
        model = Station
        fields = ['id', 'name', 'location']

class RouteSerializer(serializers.ModelSerializer):
    stop_station = StationSerializer(many=True)
    start_point = StationSerializer()
    end_point = StationSerializer()
    class Meta:
        model = Route
        fields = ['id','stop_station', 'start_point', 'end_point']

class VehicalRouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicalRoute
        fields = ['id', 'route', 'vehical', 'driver', 'state', 'active', 'date_operation']

class RegisterTripSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisterTrip
        fields = ['id', 'client', 'vehical_route', 'is_pay', 'time_outbound', 'time_return']

class VehicleTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleTicket
        fields = ['id', 'register_trip', 'vehical_route', 'time_outbound', 'time_return', 'is_pay']