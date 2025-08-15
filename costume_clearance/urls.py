"""
URL configuration for costume_clearance project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
# from clearance import views
# from core.views import CustomTokenCreateView
from django.urls import re_path
from django.views.static import serve

urlpatterns = [
    # path('aaa/jwt/create/', CustomTokenCreateView.as_view(), name='jwt-create'),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    path('admin/', admin.site.urls),
    # path('custome/',include('clearance.urls')),
    path('auth/',include('djoser.urls')),
    path('accounts/',include('core.urls')),
    path('auth/',include('djoser.urls.jwt')),
    path('Fee_calculator/', include('Fee_calculator.urls')),
    # path('clearance/', include('clearance.urls')),
    path('tree_view/', include('tariff.urls')),
    path('_nested_admin/', include('nested_admin.urls')),
    path('shipping/', include('Shipping.urls')),
    path('tracking/', include('tracking.urls')),
    path('Sea_Shipping/', include('Sea_Shipping.urls')),
    path('price/', include('price.urls')),
    path('invoice/', include('invoice.urls')),

    # path('api/create_costs/', views.CreateCosts.as_view(), name='create_costs'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
