from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from .models import Shipment
from .serializers import ShipmentSerializer
from rest_framework.response import Response

class ShipmentViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ShipmentSerializer
    queryset = Shipment.objects.all()
    lookup_field = 'id'  # Assuming 'id' is the field used for looking up shipments

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object_or_none()
        if instance:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            return Response([])

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if not queryset.exists():
            return Response([])
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_object_or_none(self):
        queryset = self.filter_queryset(self.get_queryset())
        filter_kwargs = {self.lookup_field: self.kwargs[self.lookup_field]}
        try:
            obj = queryset.get(**filter_kwargs)
            return obj
        except Shipment.DoesNotExist:
            return None
