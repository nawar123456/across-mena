from rest_framework import serializers
from .models import PortPrice , Price, Vessel




class PriceSerializer(serializers.ModelSerializer):
    # Include fields from the related Vessel model
    cuttoff_date = serializers.DateField(source='vessel.cuttoff_dare')
    date = serializers.DateField(source='vessel.date')
    end_date = serializers.DateField(source='vessel.end_date')
    number_of_station = serializers.IntegerField(source='vessel.number_of_station')
    number_of_day = serializers.IntegerField(source='vessel.number_of_day')
    solds_out=serializers.BooleanField(source='vessel.solds_out')
    class Meta:
        model = Price
        fields = ['id', 'container', 'pickup', 'port_of_origin', 'ocean_freight', 'port_of_discharge',  'cuttoff_date', 'date', 'end_date', 'number_of_station', 'number_of_day','sold_out','vessel','solds_out']


class PortPriceSerializer(serializers.ModelSerializer):
    prices = PriceSerializer(many=True, read_only=True)
    # vessel = VesselSerializer(many=True, read_only=True)

    class Meta:
        model = PortPrice
        fields = ['station_origin', 'station_delivery', 'prices', ]  
