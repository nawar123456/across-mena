from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError

from .models import AcrossMenaUser, User
from .serializers import AcrossMenaTokenCreateSerializer, AcrossMenaUserCreateSerializer,\
                    UserSerializer, AcrossMenaUserRegistrationSerializer, ResendVerificationEmailSerializer,\
                    OTPVerificationSerializer, ResendOTPSerializer
from django.utils import timezone
import requests


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class= UserSerializer
    permission_classes = [IsAuthenticated]  # Ensure that the user is authenticated

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class= UserSerializer
    permission_classes = [IsAdminUser]



### ADDED
class AcrossMenaTokenCreateView(TokenObtainPairView):
    serializer_class = AcrossMenaTokenCreateSerializer

class AcrossMenaUserCreateView(generics.CreateAPIView):
    queryset = AcrossMenaUser.objects.all()
    serializer_class = AcrossMenaUserCreateSerializer
    permission_classes=[AllowAny]

    # def post(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     across_mena_user = serializer.save()
    #     return Response(serializer.data,status=status.HTTP_201_CREATED)


class VerifyEmailView(APIView):
    def get(self, request, token):
        try:
            user = User.objects.get(verification_token=token)

            # Check if the token has expired
            if user.verification_expiry and user.verification_expiry < timezone.now():
                return Response({"message": "Verification token has expired."}, status=status.HTTP_400_BAD_REQUEST)

            user.is_verified = True
            user.verification_token = None
            user.verification_expiry = None  # Clear the expiration time after verification
            user.verification_email_resend_count = 0
            self.last_verification_email_request = None

            user.save()
            return Response({"message": "Email verified successfully."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"message": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)



# INPUT {"email":"example@email.com"}
class ResendVerificationEmailView(APIView):
    """
    View to handle the resend verification email request.
    """
    def post(self, request):
        # Validate the request data using the serializer
        serializer = ResendVerificationEmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']

            try:
                # Fetch the user by email
                user = User.objects.get(email=email)

                # Create serializer instance and call the resend logic
                user_serializer = AcrossMenaUserRegistrationSerializer()
                user_serializer.resend_verification_email(user)

                return Response({"message": "Verification email resent successfully."}, status=status.HTTP_200_OK)

            except User.DoesNotExist:
                return Response({"message": "User with this email does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


# OTP
class VerifyOTPView(APIView):
    """
    View to verify OTP based on phone number.
    """
    def post(self, request):
        serializer = OTPVerificationSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"message": "OTP verified successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResendOTPView(APIView):
    """
    View to resend OTP if conditions are met.
    """
    def post(self, request):
        serializer = ResendOTPSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"message": "OTP has been resent successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)