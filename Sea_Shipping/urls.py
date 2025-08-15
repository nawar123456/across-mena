# urls.py
from django.urls import path
from .views import FeedBackListCreateView,Contant_usListCreateView, HelperListCreateView,BookingListCreateView,SeaShippingListCreateView, LandShippingListCreateView, AirFreightListCreateView,test_translation_view

urlpatterns = [
      path('sea_shipping/', SeaShippingListCreateView.as_view(), name='sea-shipping-list-create'),

    # path('<str:lang>/sea_shipping/', SeaShippingListCreateView.as_view(), name='sea-shipping-list-create'),
   # path('sendmail/', sendmail.as_view(), name='sea-shipping-list-create'),
    path('land_shipping/', LandShippingListCreateView.as_view(), name='land-shipping-list-create'),
    path('air_freight/', AirFreightListCreateView.as_view(), name='air-freight-list-create'),
    path('booking/', BookingListCreateView.as_view(), name='BookingListCreateView'),
    path('helper/', HelperListCreateView.as_view(), name='HelperListCreateView'),
    path('contact_us/', Contant_usListCreateView.as_view(), name='Contant_usListCreateView'),
    path('FeedBack/', FeedBackListCreateView.as_view(), name='FeedBackListCreateView'),
    path('test/<str:lang>/', test_translation_view),

  #  path('customs-clearance/', CustomsClearanceListCreateView.as_view(), name='customs-clearance-list-create'),
]

