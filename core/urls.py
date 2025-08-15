from django.urls import path
from .views import AcrossMenaTokenCreateView, AcrossMenaUserCreateView,\
                   VerifyEmailView,UserDetailView,UserListView, ResendVerificationEmailView,\
                   VerifyOTPView, ResendOTPView
from rest_framework import routers
# from dj_rest_auth.views import PasswordResetView, PasswordResetConfirmView, LogoutView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
    TokenBlacklistView,
)

urlpatterns=[
    path('across-mena-register/',AcrossMenaUserCreateView.as_view(),name='acrossmena-register'),
    path('across-mena-login/',AcrossMenaTokenCreateView.as_view(),name='acrossmena-login'),
    path('across-mena-logout/', TokenBlacklistView.as_view(), name='acrossmena-logout'),
    
    path('verify-email/<str:token>/', VerifyEmailView.as_view(), name='verify_email'),
    path('resend-verification-email/', ResendVerificationEmailView.as_view(), name='resend_verification_email'),    path('profile/<str:pk>', UserDetailView.as_view(), name='profile'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('resend-otp/', ResendOTPView.as_view(), name='resend_otp'),

    # Password Reset
    # path('password/reset/', PasswordResetView.as_view(), name='password_reset'),
    # path('password/reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    # Token management
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]