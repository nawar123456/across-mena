from django.urls import path
from django.urls.conf import include
from rest_framework import routers
from . import views
from .views import PortPriceView, PriceSearchAPIView

urlpatterns = [
    path('portprice/', PortPriceView.as_view()),
    path('search/', PriceSearchAPIView.as_view(), name='price-search'),

]
