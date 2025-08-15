# serializers.py
from rest_framework import serializers
from .models import FeedBack,Contant_us,helper,Booking, Good_Air,Truck, Sea_Shipping, Land_Shipping, Air_Freight, Customs_Clearance, Container, Contant_us

class ContainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Container
        fields =  '__all__'

class TruckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Truck
        fields =  '__all__'
class GoodAirSerializer(serializers.ModelSerializer):
    class Meta:
        model = Good_Air
        fields =  '__all__'

class SeaShippingSerializer(serializers.ModelSerializer):
    containers = ContainerSerializer(many=True, read_only=True)

    class Meta:
        model = Sea_Shipping
        fields = '__all__'

class LandShippingSerializer(serializers.ModelSerializer):
    trucks = TruckSerializer(many=True, read_only=True)
    class Meta:
        model = Land_Shipping
        fields = '__all__'
        
class AirFreightSerializer(serializers.ModelSerializer):
    Good_Air = GoodAirSerializer(many=True, read_only=True)
    class Meta:
        model = Air_Freight
        fields = '__all__'

class CustomsClearanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customs_Clearance
        fields = '__all__'
        
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

class HelperSerializer(serializers.ModelSerializer):
    class Meta:
        model = helper
        fields = '__all__'

class Contant_usSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contant_us
        fields = '__all__'
        
class FeedBackSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedBack
        fields = '__all__'
