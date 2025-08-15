from django.db import models
from tree_view.models import HsCode
import random
# Create your models here.

class Sea_Shipping (models.Model):
    goods_weight = models.CharField(max_length=255,null=True, blank=True)
    goods_unit = models.CharField(max_length=255,null=True, blank=True)
    goods_type = models.CharField(max_length=900,null=True, blank=True)
    goods_description = models.CharField(max_length=900,null=True, blank=True)
    movement_type = models.CharField(max_length=900,null=True, blank=True)
    loading_address = models.CharField(max_length=255,null=True, blank=True)
    discharge_address = models.CharField(max_length=255,null=True, blank=True)
    shipment_date = models.DateField(null=True, blank=True)
    sender_name = models.CharField(max_length=100,null=True, blank=True)
    company_name = models.CharField(max_length=900,null=True, blank=True)
    phone_number = models.CharField(max_length=80,null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return f"{self.goods_type} Shipment #{self.id}"

class Container(models.Model):
    sea_shipping = models.ForeignKey(Sea_Shipping, related_name='containers', on_delete=models.CASCADE)
    container_type = models.CharField(max_length=255)
    container_number = models.CharField(max_length=255)
    length = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    Width = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    height = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)


class Land_Shipping (models.Model):
    goods_weight = models.CharField(max_length=926,null=True, blank=True)
    goods_type = models.CharField(max_length=926,null=True, blank=True)
    goods_description = models.CharField(max_length=926,null=True, blank=True)
    loading_address = models.CharField(max_length=926,null=True, blank=True)
    discharge_address = models.CharField(max_length=926,null=True, blank=True)
    goods_unit = models.CharField(max_length=20,null=True, blank=True)
    shipment_date = models.DateField(null=True, blank=True)
    sender_name = models.CharField(max_length=100,null=True, blank=True)
    company_name = models.CharField(max_length=100,null=True, blank=True)
    phone_number = models.CharField(max_length=70,null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return f"{self.goods_type} Shipment #{self.id}"

class Truck(models.Model):
    land_shipping = models.ForeignKey(Land_Shipping, related_name='truck', on_delete=models.CASCADE)
    truck_type = models.CharField(max_length=20)
    truck_number = models.CharField(max_length=20)

#📌


class Air_Freight (models.Model):
    movement_type = models.CharField(max_length=100,null=True, blank=True)
    loading_address = models.CharField(max_length=100,null=True, blank=True)
    discharge_address = models.CharField(max_length=100,null=True, blank=True)
    sender_name = models.CharField(max_length=100,null=True, blank=True)
    company_name = models.CharField(max_length=100,null=True, blank=True)
    phone_number = models.CharField(max_length=100,null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
	#📌 Note: actual_weight and volumetric_weight  should be DecimalField instead of CharField for proper numerical calculation
    #📌 Haya Error

    actual_weight = models.CharField(max_length=100,null=True, blank=True)
    volumetric_weight = models.CharField(max_length=100,null=True, blank=True)
    shipment_date = models.DateField(null=True, blank=True)
    def __str__(self):
        return f"{self.goods_type} Shipment #{self.id}"

class Good_Air(models.Model):
    air_freight = models.ForeignKey(Air_Freight, related_name='good_air', on_delete=models.CASCADE)
    goods_type = models.CharField(max_length=926,null=True, blank=True)
    goods_weight = models.CharField(max_length=80,null=True, blank=True)
    number_package = models.CharField(max_length=80,null=True, blank=True)
    Package_width = models.CharField(max_length=80,null=True, blank=True)
    Package_height = models.CharField(max_length=80,null=True, blank=True)
    Package_length = models.CharField(max_length=80,null=True, blank=True)



class Customs_Clearance (models.Model):
    SHIPMENT_TYPES = [
        ('استيراد', 'استيراد'),
        ('تصدير', 'تصدير'),
    ]

    TRANSPORTATION_TYPES = [
        ('بري', 'بري'),
        ('بحري', 'بحري'),
        ('جوي', 'جوي'),
    ]

    shipment_type = models.CharField(max_length=10, choices=SHIPMENT_TYPES)
    transportation_type = models.CharField(max_length=10, choices=TRANSPORTATION_TYPES)
    goods_weight = models.CharField(max_length=926,null=True, blank=True)
    goods_type = models.CharField(max_length=200,null=True, blank=True)
    package_type = models.CharField(max_length=200,null=True, blank=True)
    number_package = models.CharField(max_length=200,null=True, blank=True)
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    clearance_location = models.CharField(max_length=100)
    sender_name = models.CharField(max_length=100,null=True, blank=True)
    company_name = models.CharField(max_length=100,null=True, blank=True)
    phone_number = models.CharField(max_length=70,null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    def __str__(self):
        return f"{self.goods_type} Shipment #{self.id}"


class Booking (models.Model):
    direction = models.CharField(max_length=150,null=True, blank=True)
    shipping_service = models.CharField(max_length=150,null=True, blank=True)
    station_origin = models.CharField(max_length=150,null=True, blank=True)
    station_delivery = models.CharField(max_length=150,null=True, blank=True)
    ocean_freight = models.CharField(max_length=150,null=True, blank=True)
    port_of_origin = models.CharField(max_length=150,null=True, blank=True)
    port_of_destination = models.CharField(max_length=150,null=True, blank=True)
    total_price = models.CharField(max_length=150,null=True, blank=True)
    date = models.DateField()
    end_date = models.DateField()
    number_of_day = models.IntegerField()
    # commodity = models.CharField(max_length=150,null=True, blank=True)
    containers_details = models.CharField(max_length=150,null=True, blank=True)
    reference_number = models.CharField(max_length=150,null=True, blank=True)
############### NEW
    email = models.EmailField(null=True, blank=True)
    commodity = models.ForeignKey(HsCode, on_delete=models.SET_NULL, null=True, blank=True, to_field='id')    # commidity is id of an item.
    commodity_description = models.TextField(null=True)
    # weight, fullname, phone number, contact method.
    weight = models.FloatField(blank=True,null=True)
    full_name = models.CharField(max_length=255,blank=True,null=True)
    phone_number = models.CharField(max_length=255,blank=True,null=True)
    contact_method = models.CharField(max_length=255,blank=True,null=True)
    book_code = models.CharField(max_length=15, null=True)
    #book_code = models.CharField(max_length=15, null=True, unique=True)  # Ensure uniqueness
  # 📌 ERROR HAYA

    def generate_book_code(self):
        random_number = ''.join([str(random.randint(0, 9)) for _ in range(8)])
        return f"QSPOT{random_number}"

    def save(self, *args, **kwargs):
        if not self.book_code:
            self.book_code = self.generate_book_code()
        super().save(*args, **kwargs)


###############


class helper (models.Model):
    sender_name = models.CharField(max_length=100,null=True, blank=True)
    phone_number = models.CharField(max_length=100,null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    Communication_method = models.CharField(max_length=100,null=True, blank=True)
# 📌
# the C Not Capital in Communication_method
# Helper

class Contant_us (models.Model):
    sender_name = models.CharField(max_length=100,null=True, blank=True)
    phone_number = models.CharField(max_length=40,null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    massage = models.CharField(max_length=1500,null=True, blank=True)
    # second_name = models.CharField(max_length=100,null=True, blank=True)


# 📌
 #ContactUs corect name
 #Feedback name
 #tab_name
 #field_type
class FeedBack (models.Model):
    description = models.CharField(max_length=100,null=False, blank=False)
    Tab_name = models.CharField(max_length=100,null=False, blank=False)
    Field_type = models.CharField(max_length=100,null=False, blank=False)
    sender_name = models.CharField(max_length=100,null=False, blank=False)
    email = models.EmailField(null=False, blank=False)
    massage = models.CharField(max_length=1500,null=False, blank=False)
    problem = models.CharField(max_length=1500,null=True, blank=True)



