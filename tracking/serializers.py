from rest_framework import serializers
from .models import Shipment, ShipmentType, Image, ContainerDetails, Station, StationNature
from django.utils import timezone


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

class ShipmentTypeSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = ShipmentType
        fields = '__all__'

class StationnatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = StationNature
        fields = '__all__'


class StationSerializer(serializers.ModelSerializer):
    station_nature = StationnatureSerializer(many=True, read_only=True)

    class Meta:
        model = Station
        fields = '__all__'

class ContainerDetailsSerializer(serializers.ModelSerializer):
    station_set = StationSerializer(many=True, read_only=True)
    
    class Meta:
        model = ContainerDetails
        fields = '__all__'


class ShipmentSerializer(serializers.ModelSerializer):
    shipment_type = ShipmentTypeSerializer()
    containerdetails_set = ContainerDetailsSerializer(many=True, read_only=True)
    current_date = serializers.SerializerMethodField()
    current_time = serializers.SerializerMethodField()

    def get_current_date(self, obj):
        return timezone.now().strftime('%Y-%m-%d')
    
    def get_current_time(self, obj):
        return timezone.now().strftime('%H:%M:%S')
    

    class Meta:
        model = Shipment
        fields = '__all__'
