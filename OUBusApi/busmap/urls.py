from .views import UserView, BankAccountView, DriverView, ClientLoginView,ClientView, VehicleView, BusView, LocationView, StationView, RouteView, VehicalRouteView, RegisterTripView, VehicleTicketView
from django.urls import path,include
urlpatterns = [
    path('users/', UserView.as_view(), name='user-list'),
    path('drivers/', DriverView.as_view(), name='driver-list'),
    path('clients/', ClientView.as_view(), name='client-list'),
    path('clients/login/', ClientLoginView.as_view(), name='client-login'),
    path('vehicles/', VehicleView.as_view(), name='vehicle-list'),
    path('buses/', BusView.as_view(), name='bus-list'),
    path('locations/', LocationView.as_view(), name='location-list'),
    path('stations/', StationView.as_view(), name='station-list'),
    path('routes/', RouteView.as_view(), name='route-list'),
    path('vehicalroutes/', VehicalRouteView.as_view(), name='vehicalroute-list'),
    path('registertrips/', RegisterTripView.as_view(), name='registertrip-list'),
    path('vehicletickets/', VehicleTicketView.as_view(), name='vehicleticket-list'),
]