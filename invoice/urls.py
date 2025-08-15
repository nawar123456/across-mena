from django.urls import path
from invoice.views import create_invoice,invoice_success

urlpatterns = [
    path('new/', create_invoice, name='create_invoice'),
    path('success/', invoice_success, name='invoice_success'),

]