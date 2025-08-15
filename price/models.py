from django.db import models
from Fee_calculator.models import Port
from django.utils import timezone

# Create your models here.

class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(visible=True)  # Only return visible records


class PortPrice(models.Model):
    station_origin = models.ForeignKey(Port, on_delete=models.CASCADE, related_name='origin_port_prices')
    station_delivery = models.ForeignKey(Port, on_delete=models.CASCADE, related_name='delivery_port_prices')
    visible = models.BooleanField(default=True)  # 👈 NEW FIELD
    objects = ActiveManager()
    def __str__(self):
        return f"{self.station_origin} - {self.station_delivery}"

class Vessel(models.Model):
    date = models.DateField()
    cuttoff_dare = models.DateField()
    end_date = models.DateField()
    number_of_station = models.IntegerField()
    number_of_day = models.IntegerField()
    port_price = models.ForeignKey(PortPrice, on_delete=models.CASCADE, related_name="vessels")
    solds_out=models.BooleanField(default=False, null=False, blank=True)

    def __str__(self):
        return f"{self.number_of_station} - {self.number_of_day}"



from django.db import models

class Price(models.Model):
    CONTAINER_CHOICES = [
        ('20ft', '20ft'),
        ('40ft', '40ft'),
        ('20ft Fresser', '20ft Fresser'),
        ('40HC', '40HC'),
    ]
    vessel = models.ForeignKey('Vessel', on_delete=models.CASCADE, related_name='prices')
    container = models.CharField(max_length=255, choices=CONTAINER_CHOICES,null=True,blank=True)
    pickup = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    port_of_origin = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    ocean_freight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    port_of_discharge = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    added_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    ocean_freight_last_updated = models.DateTimeField(null=True, blank=True)  # 👈 NEW
    sold_out=models.BooleanField(default=False, null=False, blank=True)

    def __str__(self):
        return f"{self.container} - {self.vessel}"

    def save(self, *args, **kwargs):
        self.added_value = self.added_value or 0
        self.ocean_freight = self.ocean_freight or 0
        # only update timestamp if ocean_freight changed
        if self.pk:
            old = Price.objects.get(pk=self.pk)
            delta = self.added_value - (old.added_value or 0)
            self.ocean_freight += self.added_value
            if old.ocean_freight != self.ocean_freight:
                self.ocean_freight_last_updated = timezone.now()
                
        else:
            self.ocean_freight_last_updated = timezone.now()
            self.ocean_freight += self.added_value

        super().save(*args, **kwargs)

        if self.container == '40HC':
            exists = Price.objects.filter(vessel=self.vessel, container='40ft').exists()
            if not exists:
                Price.objects.create(
                    vessel=self.vessel,
                    container='40ft',
                    pickup=self.pickup,
                    port_of_origin=self.port_of_origin,
                    ocean_freight=self.ocean_freight - self.added_value,
                    port_of_discharge=self.port_of_discharge,
                    added_value =self.added_value,
                    
                )

        # if self.container == '20ft':
        #     exists = Price.objects.filter(vessel=self.vessel, container='20ft').exists()
        #     if not exists:
        #         Price.objects.create(
        #             vessel=self.vessel,
        #             container='20ft',
        #             pickup=self.pickup,
        #             port_of_origin=self.port_of_origin,
        #             ocean_freight=self.ocean_freight - self.added_value,
        #             port_of_discharge=self.port_of_discharge,
        #             added_value =self.added_value,
                    
        #         )      