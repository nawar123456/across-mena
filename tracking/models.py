from django.db import models

# Create your models here.

class Shipment(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    shipment_type = models.ForeignKey('ShipmentType', on_delete=models.CASCADE)
    assign_stations = models.BooleanField() 
    number_of_container = models.CharField(max_length=255,null=True, blank=True)
    number_of_packages = models.CharField(max_length=255,null=True, blank=True)
    Total_gross_weight =  models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    General_type_goods =  models.CharField(max_length=512, null=True, blank=True)


    def __str__(self):
        return self.id

class ShipmentType(models.Model):
    type = models.CharField(max_length=255, null=True, blank=True)
    images = models.ManyToManyField('Image', blank=True)
    def __str__(self):
        return self.type

class Image(models.Model):
    id = models.IntegerField(primary_key=True)
    image = models.FileField(upload_to='media/track')
   

 

class ContainerDetails(models.Model):
    CONTENT_CHOICES = (
        ('20 FT', '20 FT'),
        ('40 FT', '40 FT'),
        ('40 HC', '40 HC'),
        ('20 HC', '20 HC'),
    )
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE)
    container_number = models.CharField(max_length=255,null=True, blank=True)
    container_type = models.CharField(max_length=255,null=True, blank=True, choices=CONTENT_CHOICES)
    type_of_goods = models.CharField(max_length=255,null=True, blank=True)
    number_of_packages_in_container = models.CharField(max_length=255,null=True, blank=True)
    gross_weight =  models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)

    def __str__(self):
        return self.container_number


class Station(models.Model):
    container = models.ForeignKey(ContainerDetails, on_delete=models.CASCADE, null=True, blank=True)
    station_name = models.CharField(max_length=255, null=True, blank=True)

    CONTENT_CHOICES = (
        ('ترانزيت', 'ترانزيت'),
        ('رئيسي', 'رئيسي'),
    )

    station_type = models.CharField(max_length=255, choices=CONTENT_CHOICES)
    transportation_name = models.CharField(max_length=255,null=True, blank=True)
    station_nature = models.ManyToManyField('StationNature')
    arrival_date = models.DateField(null=True, blank=True)  
    gatein_date = models.DateField(null=True, blank=True)  

    def get_station_nature(self):
        try:
            return self.stationnature.type_station
        except StationNature.DoesNotExist:
            return "N/A"


class StationNature(models.Model):
    type_station = models.CharField(max_length=255, null=True, blank=True)
    image_station = models.FileField(upload_to='media/track')
    

    def __str__(self):
        return self.type_station if self.type_station else "N/A"
 

