from django.contrib import admin
from nested_admin import nested
from .models import Shipment, ContainerDetails, Station, StationNature, ShipmentType

class StationInline(nested.NestedTabularInline):
    model = Station
    extra = 0


class ContainerDetailsInline(nested.NestedTabularInline):
    model = ContainerDetails
    extra = 0
    inlines = [StationInline]

class ShipmentAdmin(nested.NestedModelAdmin):
    list_display = ('id', 'shipment_type', 'assign_stations', 'number_of_container', 'number_of_packages', 'Total_gross_weight')
    inlines = [ContainerDetailsInline]

admin.site.register(Shipment, ShipmentAdmin)
admin.site.register(ShipmentType)
admin.site.register(StationNature)
