from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum
from django.db.models import ExpressionWrapper, F, DecimalField
from rest_framework import generics
from .models import Price, PortPrice
from .serializers import PriceSerializer, PortPriceSerializer
from rest_framework import status
from django.db.models import Q
from datetime import timedelta, date
from Fee_calculator.models import Port



class PortPriceView(APIView):
    def get(self, request, format=None):
        type_of_transportation = request.query_params.get('type', None)
        station_origin = request.query_params.get('station_origin', None)
        station_delivery = request.query_params.get('station_delivery', None)

        if type_of_transportation == 'door_to_door':
            queryset = PortPrice.objects.filter(station_origin=station_origin, station_delivery=station_delivery)
            # total_price = queryset.aggregate(total_price=ExpressionWrapper(Sum(F('ocean_freight') + F('port_of_origin')), output_field=DecimalField()))['total_price']
            #return Response({'total_price': total_price})
        else:
            return Response({'error': 'Invalid type of transportation'})


""" 
class PriceSearchAPIView(generics.ListAPIView):
    serializer_class = PriceSerializer

    def get_queryset(self):
        station_origin = self.request.query_params.get('station_origin', None)
        station_delivery = self.request.query_params.get('station_delivery', None)
        container = self.request.query_params.get('container', None)

        if not station_origin or not station_delivery or not container:
            return Price.objects.none()

        try:
            port_price = PortPrice.objects.get(
                station_origin__name=station_origin,
                station_delivery__name=station_delivery
            )
        except PortPrice.DoesNotExist:
            return Price.objects.none()

        queryset = Price.objects.filter(
            vessel__port_price=port_price,
            container=container
        )

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
""" 
class PriceSearchAPIView(generics.ListAPIView):
    serializer_class = PriceSerializer

    def get_queryset(self):
        station_origin = self.request.query_params.get('station_origin', None)
        station_delivery = self.request.query_params.get('station_delivery', None)
        container = self.request.query_params.get('container', None)

        if not station_origin or not station_delivery or not container:
            return Price.objects.none()

        try:
            # Retrieve the Port objects based on port_code instead of name
            port_origin = Port.objects.get(port_code=station_origin)
            port_delivery = Port.objects.get(port_code=station_delivery)

            port_price = PortPrice.objects.get(
                station_origin=port_origin,
                station_delivery=port_delivery
            )
        except (Port.DoesNotExist, PortPrice.DoesNotExist):
            return Price.objects.none()

        queryset = Price.objects.filter(
            vessel__port_price=port_price,
            container=container
        )

        return queryset
# من هون منحذف مشان ما بقى يضيف للتاريخ الللي خلص 

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
    
        # # Get current date
        # current_date = date.today()
    
        # # Loop through queryset and modify data
        # for price in queryset:
        #     while price.vessel.date <= current_date + timedelta(days=3):
        #         # Modify start date and end date by adding 7 days
        #         price.vessel.date += timedelta(days=7)
        #         price.vessel.end_date += timedelta(days=10)
        #         # Check if ID is even
        #         if price.id % 2 == 0:
        #             # Add $50 to the price
        #             price.pickup += 50
        #             price.ocean_freight += 50
        #         else:
        #             # Add $20 to the price
        #             price.pickup += 20
        #             price.ocean_freight += 20
    
        # # Serialize modified data
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


