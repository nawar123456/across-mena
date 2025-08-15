from django.db.models import Q
from django.core.mail import send_mail
from django.urls import reverse
# from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import ValidationError
from .models import User, AcrossMenaUser
from Fee_calculator.models import Origin
import re
import uuid
import phonenumbers
from phonenumbers import NumberParseException
import requests
from urllib.parse import quote
from django.utils import timezone
import datetime
from djoser.serializers import UserSerializer as BaseUserSerializer ,UserCreateSerializer as BaseUserRegistrationSerializer

# class UpdateUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['email','phone_number','first_name','last_name']
        
# class CreateUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['username','first_name','last_name','email','phone_number']

            
class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id' , 'first_name','last_name', 'phone','image','trader','costumebroker'] 


### ADDED

# Constants for regex patterns for email validation
EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

class AcrossMenaUserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['email', 'phone', 'first_name', 'last_name', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True},
            'confirm_password': {'write_only': True}
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def validate(self, attrs):
        # Check if passwords match
        if attrs['password'] != attrs['confirm_password']:
            raise ValidationError({"password": "Passwords do not match."})

        # Validate the password using Django's validators
        try:
            validate_password(attrs['password'])
        except ValidationError as e:
            raise ValidationError({"password": list(e.messages)})

        # Validate phone number
        phone = attrs.get('phone')
        self.is_valid_phone(phone)

        return attrs

    def save(self, **kwargs):
        email = self.validated_data.get('email')
        phone = self.validated_data.get('phone')
        self.validated_data.pop('confirm_password')  # Remove confirm_password after validation

        # Create the user and set initial values
        user = User(email=email, phone=phone, first_name=self.validated_data.get('first_name'), last_name=self.validated_data.get('last_name'))
        user.set_password(self.validated_data['password'])
        user.is_verified = False  # Set is_verified to False initially
        user.save()
    
        # Check if the phone number is Syrian
        if self.is_syrian_phone(phone):
            self.send_otp_phone_verification(user)
        else:
            # Send email verification for non-Syrian numbers
            self.send_verification_email(user)

        return user

    def resend_verification_email(self, user):
        """Handles the resend verification email logic with resend count and cooldown periods."""
        if user.is_verified:
            raise ValidationError({"detail": "This account is already verified."})

        # Define cooldown periods based on resend count
        cooldown_period = 0  # Default for the first attempt
        if user.verification_email_resend_count == 1:
            cooldown_period = 5  # 5 minutes for the second attempt
        elif user.verification_email_resend_count >= 2:
            cooldown_period = 60  # 60 minutes for subsequent attempts

        # Check if enough time has passed since the last request
        if user.last_verification_email_request:
            time_since_last_request = (timezone.now() - user.last_verification_email_request).total_seconds() / 60
            if time_since_last_request < cooldown_period:
                minutes_left = int(cooldown_period - time_since_last_request)
                raise ValidationError({"detail": f"Please wait for {minutes_left} minutes to resend the verification email."})

        # Update resend count and last request time
        user.verification_email_resend_count += 1
        user.last_verification_email_request = timezone.now()
        user.save()

        # Generate a new token if needed and send the verification email
        # if user.verification_expiry and user.verification_expiry > timezone.now():
        #     raise ValidationError({"detail": "The verification token is still valid, please check your inbox."})
        
        user.verification_token = str(uuid.uuid4())
        user.verification_expiry = timezone.now() + datetime.timedelta(hours=24)
        user.save()

        # Send the verification email
        self.send_verification_email(user)

    @staticmethod
    def is_syrian_phone(phone):
        """Check if the phone number belongs to Syria (starts with +963)."""
        return phone.startswith('+963')

    @staticmethod
    def is_valid_email(email):
        """Validate the email format using regex."""
        return re.match(EMAIL_REGEX, email) is not None

    @staticmethod
    def is_valid_phone(phone):
        """Validates the phone number format."""
        # Ensure the phone starts with '+'
        if not phone.startswith('+'):
            raise ValidationError({"phone": "Phone number must start with '+' followed by the country code."})

        # If the phone number is Syrian, enforce further checks
        if AcrossMenaUserRegistrationSerializer.is_syrian_phone(phone):
            try:
                parsed = phonenumbers.parse(phone, None)

                # Check if the country code is +963 for Syria
                if parsed.country_code != 963:
                    raise ValidationError({"phone": "Only Syrian phone numbers (+963) are allowed."})

                # Validate the phone number format
                if not phonenumbers.is_valid_number(parsed):
                    raise ValidationError({"phone": "Invalid phone number format."})

                # Ensure that it starts with +963 followed by 9 digits, not starting with 0
                if not re.match(r'^\+963[1-9]\d{8}$', phone):
                    raise ValidationError({"phone": "Phone number format must be: +963 followed by 9 digits, and should not start with 0 after the country code."})

            except NumberParseException:
                raise ValidationError({"phone": "Invalid phone number format."})

        return True

    def send_otp_phone_verification(self, user):
        """Send OTP to the Syrian phone number (future implementation)."""
        user.generate_otp()  # Generate a new OTP
        user.send_otp_mtn()  # Send the OTP via the MTN API

    def send_verification_email(self, user):
        """Send email verification for non-Syrian numbers."""
        token = str(uuid.uuid4())
        user.verification_token = token
        user.save()

        email_subject, email_message = self._construct_verification_email(user, token)
        send_mail(email_subject, email_message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)

    def _construct_verification_email(self, user, token):
        """Construct the verification email."""
        # current_site = get_current_site(self.request)
        verification_url = f"https://across-mena.com{reverse('verify_email', args=[token])}"

        email_subject = 'Email Verification'
        email_message = (
            f'Please verify your email.\n'
            f'For verification, visit this URL:\n'
            f'{verification_url}'
        )
        return email_subject, email_message


class AcrossMenaUserCreateSerializer(serializers.ModelSerializer):
    user = AcrossMenaUserRegistrationSerializer()
    country = serializers.PrimaryKeyRelatedField(queryset=Origin.objects.all())

    class Meta:
        model = AcrossMenaUser
        fields = ['id', 'user', 'company_name', 'country']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        country = validated_data.pop('country')

        user_serializer = AcrossMenaUserRegistrationSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        across_mena_user = AcrossMenaUser.objects.create(user=user, country=country, **validated_data)
        return across_mena_user


class AcrossMenaTokenCreateSerializer(TokenObtainPairSerializer):
    email_or_phone = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('username', None)  # We are not using the 'username' field

    def validate(self, attrs):
        email_or_phone = attrs.get("email_or_phone")
        password = attrs.get("password")

        # Find the user by either email or phone number
        user = self.get_user(email_or_phone)

        # Check if the user is verified
        if not user.is_verified:
            raise ValidationError({"detail": "Your account is not verified. Please verify your email or phone to log in."})

        # Prepare credentials for authentication
        credentials = {
            'username': user.username,  # We use the username internally for auth
            'password': password,
        }

        # Authenticate user based on email or phone
        if AcrossMenaUserRegistrationSerializer.is_valid_email(email_or_phone):
            credentials['email'] = email_or_phone
        elif AcrossMenaUserRegistrationSerializer.is_valid_phone(email_or_phone):
            credentials['phone'] = email_or_phone
        else:
            raise ValidationError({"email_or_phone": "Invalid email or phone!"})

        # Call the superclass validate method for token generation
        data = super().validate(credentials)
        refresh = self.get_token(self.user)

        # Return the access and refresh tokens
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        return data

    def get_user(self, email_or_phone):
        """
        This method finds the user based on the email or phone number provided.
        """
        try:
            return User.objects.get(Q(email=email_or_phone) | Q(phone=email_or_phone))
        except User.DoesNotExist:
            raise ValidationError({"email_or_phone": "Invalid email or phone or password!"})



# Resend Email.
class ResendVerificationEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


# OTP VERIFICATION:
class OTPVerificationSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=255)
    otp_code = serializers.CharField(max_length=4, required=True)

    def validate(self, attrs):
        phone = attrs.get('phone')
        otp_code = attrs.get('otp_code')
        
        try:
            user = User.objects.get(phone=phone)

            # Attempt OTP verification
            is_valid, message = user.verify_otp(otp_code)
            if not is_valid:
                raise ValidationError({"otp_code": message})

            return attrs

        except User.DoesNotExist:
            raise ValidationError({"phone": "No account found with this phone number."})
        

class ResendOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=255)

    def validate(self, attrs):
        phone = attrs.get('phone')
        
        try:
            user = User.objects.get(phone=phone)

            # Check if the user can resend the OTP based on cooldown and attempt conditions
            can_resend, message = user.can_resend_otp()
            if not can_resend:
                raise ValidationError({"phone": message})

            # Generate and send OTP if conditions are met
            user.request_otp()
            return attrs

        except User.DoesNotExist:
            raise ValidationError({"phone": "No account found with this phone number."})