
from rest_framework.routers import DefaultRouter
from rest_framework import routers
from django.urls import path, include
from .views import ShipmentViewSet



router = routers.DefaultRouter()
router.register(r'shipments', ShipmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
   


]
