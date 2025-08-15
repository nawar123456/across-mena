from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.Sea_Shipping)
class Sea_ShippingAdmin(admin.ModelAdmin):
    search_fields = ['id', 'sender_name', 'email']
    list_display = ['id', 'sender_name', 'email']

@admin.register(models.Land_Shipping)
class Land_ShippingAdmin(admin.ModelAdmin):
    search_fields = ['id', 'sender_name', 'email']
    list_display = ['id', 'sender_name', 'email']

@admin.register(models.Air_Freight)
class Air_FreightAdmin(admin.ModelAdmin):
    search_fields = ['id', 'sender_name', 'email']
    list_display = ['id', 'sender_name', 'email']

@admin.register(models.Customs_Clearance)
class Customs_ClearanceAdmin(admin.ModelAdmin):
    search_fields = ['id', 'sender_name', 'email']
    list_display = ['id', 'sender_name', 'email']


@admin.register(models.helper)
class HelperAdmin(admin.ModelAdmin):
    search_fields = ['id', 'sender_name', 'email']
    list_display = ['id', 'sender_name', 'email']
    
admin.site.register(models.Booking)