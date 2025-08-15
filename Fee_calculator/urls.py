from django.urls import path
from django.urls.conf import include
from rest_framework import routers
from . import views
from rest_framework.routers import SimpleRouter
from .views import calculate_view, OriginListAPIView, SearchView, CalculateViewSet, AirportView

router = SimpleRouter()
router.register('fees', views.FeesViewSet, basename='fees')
router.register('origin', views.OriginViewSet, basename='origin')
router.register('extra', views.ExtraViewSet, basename='extra')
# URLConf
urlpatterns = router.urls 

urlpatterns = router.urls + [
    path('calculate/', views.calculate_view, name='calculate'),
    path('origin_port/<str:language>/<str:origin>/', OriginListAPIView.as_view(), name='country-detail'),
    path('search/', SearchView.as_view(), name='search_view'),
    path('multi_calculate/',  CalculateViewSet.calculate_view, name='calculate'), 
    path('airport/', AirportView.as_view(), name='search_view'),


 
]