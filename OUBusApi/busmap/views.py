from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
import logging
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.parsers import JSONParser,MultiPartParser
from rest_framework.exceptions import ParseError
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, BankAccount, Driver, Client, Vehicle, Bus, Location, Station, Route, VehicalRoute, RegisterTrip, VehicleTicket
from .serializers import UserSerializer, BankAccountSerializer, DriverSerializer, ClientSerializer, VehicleSerializer, BusSerializer, LocationSerializer, StationSerializer, RouteSerializer, VehicalRouteSerializer, RegisterTripSerializer, VehicleTicketSerializer
from django.core.files.storage import default_storage

@method_decorator(csrf_exempt, name='dispatch')
class UserView(View):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    def put(self, request):
        data = JSONParser().parse(request)
        user = User.objects.get(id=data['id'])
        serializer = UserSerializer(user, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse("Updated Successfully!!", safe=False)
        return JsonResponse("Failed to Update.", safe=False)

    def delete(self, request, id):
        user = User.objects.get(id=id)
        user.delete()
        return JsonResponse("Deleted Successfully!!", safe=False)

@method_decorator(csrf_exempt, name='dispatch')
class BankAccountView(View):

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = BankAccountSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    def put(self, request):
        data = JSONParser().parse(request)
        user = User.objects.get(id=data['id'])
        serializer = UserSerializer(user, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse("Updated Successfully!!", safe=False)
        return JsonResponse("Failed to Update.", safe=False)

    def delete(self, request, id):
        user = User.objects.get(id=id)
        user.delete()
        return JsonResponse("Deleted Successfully!!", safe=False)

@method_decorator(csrf_exempt, name='dispatch')
class DriverView(View):
    def get(self, request):
        drivers = Driver.objects.all()
        serializer = DriverSerializer(drivers, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = DriverSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    def put(self, request):
        data = JSONParser().parse(request)
        user = User.objects.get(id=data['id'])
        serializer = UserSerializer(user, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse("Updated Successfully!!", safe=False)
        return JsonResponse("Failed to Update.", safe=False)

    def delete(self, request, id):
        user = User.objects.get(id=id)
        user.delete()
        return JsonResponse("Deleted Successfully!!", safe=False)
logger = logging.getLogger(__name__)
@method_decorator(csrf_exempt, name='dispatch')
class ClientView(View):
    def get(self, request):
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        try:
            data = request.POST.dict()
            files = request.FILES
            print(files)
            if 'avatar' in files:
                data['avatar'] = files['avatar']

            # Tạo đối tượng User
            username = data.get('username')
            password = data.get('password')
            if not username or not password:
                return JsonResponse({'error': 'Username and password are required'}, status=400)

            if Client.objects.filter(username=username).exists():
                return JsonResponse({'error': 'Username already exists'}, status=400)

            user = Client(username=username)
            user.set_password(password)  # Mã hóa mật khẩu
            user.save()

            # Tạo đối tượng Client với dữ liệu từ serializer
            serializer = ClientSerializer(data=data)
            if serializer.is_valid():
                serializer.save(user=user)  # Liên kết đối tượng User với Client
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)
        except ParseError as e:
            logger.error(f"Parse error in POST: {e}")
            return JsonResponse({'error': 'JSON parse error'}, status=400)
        except Exception as e:
            logger.error(f"Unexpected error in POST: {e}")
            return JsonResponse({'error': 'Internal server error'}, status=500)
    def put(self, request):
        data = JSONParser().parse(request)
        user = User.objects.get(id=data['id'])
        serializer = UserSerializer(user, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse("Updated Successfully!!", safe=False)
        return JsonResponse("Failed to Update.", safe=False)

    def delete(self, request, id):
        user = User.objects.get(id=id)
        user.delete()
        return JsonResponse("Deleted Successfully!!", safe=False)

@method_decorator(csrf_exempt, name='dispatch')
class ClientLoginView(APIView):
     def post(self, request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            print(username, password)
            if not username or not password:
                return JsonResponse({'error': 'Username and password are required'}, status=400)

            # Kiểm tra người dùng trong cơ sở dữ liệu
            user = User.objects.filter(username=username).first()
            print(user)
            if not user:
                return JsonResponse({'error': 'User not found'}, status=400)

            # Kiểm tra mật khẩu
            if not user.check_password(password):
                return JsonResponse({'error': 'Incorrect password'}, status=400)

            # Kiểm tra trạng thái kích hoạt
            if not user.is_active:
                return JsonResponse({'error': 'User is not active'}, status=400)

            # Xác thực người dùng
            user = authenticate(username=username, password=password)
            print(user)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                return JsonResponse({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=200)
            else:
                return JsonResponse({'error': 'Invalid username or password'}, status=400)
        except Exception as e:
            logger.error(f"Unexpected error in login: {e}")
            return JsonResponse({'error': 'Internal server error'}, status=500)
@method_decorator(csrf_exempt, name='dispatch')
class VehicleView(View):
    def get(self, request):
        vehicles = Vehicle.objects.all()
        serializer = VehicleSerializer(vehicles, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = VehicleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class BusView(View):
    def get(self, request):
        buses = Bus.objects.all()
        serializer = BusSerializer(buses, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = BusSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class LocationView(View):
    def get(self, request):
        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = LocationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class StationView(View):
    def get(self, request):
        stations = Station.objects.all()
        serializer = StationSerializer(stations, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = StationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class RouteView(View):
    def get(self, request):
        routes = Route.objects.all().select_related('start_point', 'end_point').prefetch_related('stop_station')
        serializer = RouteSerializer(routes, many=True)
        print(serializer.data)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = RouteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class VehicalRouteView(View):
    def get(self, request):
        vehical_routes = VehicalRoute.objects.all()
        serializer = VehicalRouteSerializer(vehical_routes, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = VehicalRouteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class RegisterTripView(View):
    def get(self, request):
        register_trips = RegisterTrip.objects.all()
        serializer = RegisterTripSerializer(register_trips, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = RegisterTripSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class VehicleTicketView(View):
    def get(self, request):
        vehicle_tickets = VehicleTicket.objects.all()
        serializer = VehicleTicketSerializer(vehicle_tickets, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = VehicleTicketSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
@csrf_exempt
def saveFile(request):
    file=request.FILES['file']
    filename=default_storage.save(file.name, file)
    return JsonResponse(filename, safe=False)