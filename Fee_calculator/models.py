from django.db import models
from django.core.exceptions import ObjectDoesNotExist  

# Create your models here.
class Fees (models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    label_en = models.CharField(max_length=1024)
    label = models.CharField(max_length=1024)
    export1 = models.CharField(max_length=255)
    fee = models.DecimalField(max_digits=10, decimal_places=4)
    spending_fee = models.DecimalField(max_digits=10, decimal_places=4)
    support_fee = models.DecimalField(max_digits=10, decimal_places=4)
    protection_fee = models.DecimalField(max_digits=10, decimal_places=4)
    natural_fee = models.DecimalField(max_digits=10, decimal_places=4)
    tax_fee = models.DecimalField(max_digits=10, decimal_places=4)
    local_fee = models.DecimalField(max_digits=10, decimal_places=4)
    gold = models.DecimalField(max_digits=10, decimal_places=4)
    paper = models.DecimalField(max_digits=10, decimal_places=4)
    brid = models.DecimalField(max_digits=10, decimal_places=4)
    price = models.DecimalField(max_digits=10, decimal_places=4)
    unit = models.CharField(max_length=255)
    unit_en = models.CharField(max_length=255)
    feesGroup = models.ManyToManyField("FeesGroup", blank=True)
    Import_fee = models.DecimalField(max_digits=10, decimal_places=4, default=0.01)
    placeholder=models.CharField(max_length=255,  blank=True, null=True)
    placeholder_en=models.CharField(max_length=255,  blank=True, null=True)
    dolar= models.ForeignKey('Dolar', on_delete=models.CASCADE, db_column='dolar_id')
    total_taxes = models.ForeignKey('Taxes', on_delete=models.CASCADE, db_column='taxes_id')
    decision = models.CharField(max_length=4024 ,blank=True, null=True)
    decision_en = models.CharField(max_length=4024 ,blank=True, null=True)




    def __str__(self) -> str:
        return self.label
class FeesGroup (models.Model):
    id = models.IntegerField(primary_key=True)
    label = models.CharField(max_length=255)
    def __str__(self) -> str:
        return self.label


class Origin (models.Model):
    AR = 'ar'
    EN = 'en'
    LANGUAGE = [
        (AR,'عربي'),
        (EN,'english'),
    ]
    lang = models.CharField(max_length=2,choices=LANGUAGE,default=AR)
    label = models.CharField(max_length=255)
    label_ar = models.CharField(max_length=255,null=True, blank=True)
    ImageURL =models.CharField(max_length=255)
    countries_code = models.CharField(max_length=255)
    countryGroups = models.ManyToManyField("CountryGroup")
    def __str__(self) -> str:
        return self.label
class CountryGroup (models.Model):
    label = models.CharField(max_length=255)
    def __str__(self) -> str:
        return self.label



class Port(models.Model):
    countries_code = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    name_arabic = models.CharField(max_length=255)
    port_code = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        try:
            self.origin = Origin.objects.get(countries_code=self.countries_code)
        except ObjectDoesNotExist:
            self.origin = None  # ✅ Prevent crash by setting to None instead of failing

        super(Port, self).save(*args, **kwargs)


class Airport(models.Model):
    countries_code = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    name_arabic = models.CharField(max_length=255)
    airport_code = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Retrieve the Origin object based on countries_code
        origin_obj = Origin.objects.get(countries_code=self.countries_code)

        # Set the country field using the retrieved Origin object
        self.country = origin_obj # ERROR the Aitport Model dont have a country field !!
		# 1)solve: make FK with Origin.country

		#, the super() function is used to call methods from a parent or superclass from within a child or subclass.
		#  It's particularly useful in inheritance scenarios.
        super(Port, self).save(*args, **kwargs) # the goal is call the save() method
		#ERROR should super(Airport, self).save(*args, **kwargs)
		#or super().save(*args, **kwargs)
		#📌 Haya Error





class Extra(models.Model):
    fees = models.ForeignKey(Fees, on_delete=models.CASCADE, related_name="extras",null=True)
	#automaticlly add _id cause the relation
	#('Dolar', on_delete=models.CASCADE, db_column='dolar_id') sgape for name of FK
    label = models.CharField(max_length=255,null=True, blank=True)
    label_en = models.CharField(max_length=255,null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=5,null=True, blank=True)
    origin = models.ManyToManyField(Origin, blank=True)
    countryGroups = models.ManyToManyField(CountryGroup, blank=True)
    lycra = models.BooleanField(default=False)
    colored_thread = models.BooleanField(default=False)
    Brand = models.BooleanField(default=False)
    tubes  =models.BooleanField(default=False)

class Taxes(models.Model):
    label = models.CharField(max_length=1024)
    price = models.DecimalField(max_digits=25, decimal_places=4)

class Dolar(models.Model):
    price = models.DecimalField(max_digits=25, decimal_places=4)


class Atom(models.Model):
    categories = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=4)


class Export_Price(models.Model):
    fees_id = models.ForeignKey(Fees, on_delete=models.CASCADE, related_name="export_price",null=True, blank=True)
    name=  models.CharField(max_length=255,null=True, blank=True)
    unit =  models.CharField(max_length=25,null=True, blank=True)
    decision = models.CharField(max_length=4024,null=True, blank=True)
    Lowest_price =  models.CharField(max_length=25,null=True, blank=True)
    highest_price =  models.CharField(max_length=25,null=True, blank=True)
    price =  models.CharField(max_length=25,null=True, blank=True)
    notes =  models.CharField(max_length=250,null=True, blank=True)
    def __str__(self) -> str:
        return self.name











