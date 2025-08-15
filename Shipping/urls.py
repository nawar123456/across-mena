from django.urls import path, include
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('api/send-email/', views.send_email, name='send_email'),
    path('receive-emails/', views.fetch_emails, name='receive_emails'),
   

]
