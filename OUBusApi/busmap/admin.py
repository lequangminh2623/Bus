from django.contrib import admin
from busmap.models import Location, Station, Route, Vehicle, Bus, Driver, VehicalRoute, RegisterTrip, BankAccount, User, Client,VehicleTicket
from django.utils.html import  mark_safe
class VehicalAdmin(admin.ModelAdmin):
    list_display = ['id','seat_number','plate_number','driver']
    search_fields = ['id']
    list_filter = ['id','seat_number','plate_number']
    readonly_fields = ['avatar']
    def avatar(self,vehical):
        return mark_safe(f"<img src='/static/{vehical.image.name}' width='120' />")
    class Media:
        css = {
            'all': ('/static/css/styles.css',)
        }

        js = ('/static/js/script.js',)
class RouteAdmin(admin.ModelAdmin):
    ist_display = ['id', 'get_stop_stations', 'start_point', 'end_point']
    search_fields = ['start_point__name', 'end_point__name']
    list_filter = ['id', 'start_point', 'end_point']
    readonly_fields = ['id']
    def get_stop_stations(self, obj):
        return ", ".join([station.name for station in obj.stop_station.all()])
    get_stop_stations.short_description = 'Stop Stations'
    def avatar(self,route):
        return mark_safe(f"<img src='/static/{route.image.name}' width='120' />")
    class Media:
        css = {
            'all': ('/static/css/styles.css',)
        }
        js = ('/static/js/script.js',)
admin.site.register(Location)
admin.site.register(Vehicle,VehicalAdmin)
admin.site.register(Route,RouteAdmin)
admin.site.register(Station)
admin.site.register(Bus)
admin.site.register(Driver)
admin.site.register(VehicalRoute)
admin.site.register(BankAccount)
admin.site.register(User)
admin.site.register(Client)
admin.site.register(VehicleTicket)
admin.site.register(RegisterTrip)
# Register your models here.
