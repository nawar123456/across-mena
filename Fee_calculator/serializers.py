from .models import Extra, Fees, Origin, Dolar, Taxes, Atom, Port, Airport
from rest_framework import serializers
from django.db.models import Sum 



class OriginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Origin
        fields = ['id','label', 'label_ar','ImageURL', 'countries_code', 'countryGroups']


class ExtraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Extra
        fields = '__all__'
    def to_representation(self, instance):
        lang_header = self.context['request'].headers.get('Language', 'ar')
        data = super().to_representation(instance)
        if lang_header == 'en':
            # If language is English, replace Arabic fields with English fields
            data['label'] = data['label_en']
            # Remove the redundant English fields
            data.pop('label_en', None)
        else:
            # If language is Arabic, remove English fields
            data.pop('label_en', None)
        return data


class DolarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dolar
        fields = ['price']

class TotalTaxesSerializer(serializers.ModelSerializer):
    total_tax = serializers.SerializerMethodField()
    partial_tax = serializers.SerializerMethodField()
    arabic_stamp = serializers.SerializerMethodField()

    class Meta:
        model = Taxes
        fields = ['total_tax', 'partial_tax', 'arabic_stamp']

    def get_total_tax(self, obj):
        specific_taxes = Taxes.objects.filter(id__in=[1, 3, 4, 5, 6])
        total_tax = specific_taxes.aggregate(total_tax=Sum('price'))['total_tax']
        return total_tax

    def get_partial_tax(self, obj):
        specific_taxes = Taxes.objects.filter(id__in=[1, 4, 5, 6, 8])
        partial = specific_taxes.aggregate(partial_tax=Sum('price'))['partial_tax']
        return partial

    def get_arabic_stamp(self, obj):
        specific_taxes = Taxes.objects.filter(id__in=[8])
        arabic_stamp = specific_taxes.aggregate(arabic_stamp=Sum('price'))['arabic_stamp']
        return arabic_stamp
        
class FeesSerializer(serializers.ModelSerializer):
    extras = ExtraSerializer(many=True)
    dolar = DolarSerializer()  
    total_taxes = TotalTaxesSerializer()  

    class Meta:
        model = Fees
        fields = '__all__'
    # def to_representation(self, instance):
    #     lang_header = self.context['request'].headers.get('Language', 'ar')
    #     data = super().to_representation(instance)

    #     if lang_header == 'en':
    #         # If language is English, replace Arabic fields with English fields
    #         data['label'] = data['label_en']
    #         data['placeholder'] = data['placeholder_en']
    #         data['decision'] = data['decision_en']

    #         # Remove the redundant English fields
    #         data.pop('label_en', None)
    #         data.pop('placeholder_en', None)
    #         data.pop('decision_en', None)
    #     else:
    #         # If language is Arabic, remove English fields
    #         data.pop('label_en', None)
    #         data.pop('placeholder_en', None)
    #         data.pop('decision_en', None)

    #     return data

class AtomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Atom
        fields = ['price']

class PortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Port
        fields = ['name','name_arabic']

class airPortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ['name','name_arabic']



class CountrySerializer(serializers.ModelSerializer):
    ports = PortSerializer(many=True, read_only=True)

    class Meta:
        model = Origin
        fields = ['label', 'ImageURL', 'ports']
