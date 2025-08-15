from django.db import models
from django.db.models import Q
from django.contrib.auth.models import AbstractUser, UserManager
from django.conf import settings
from django.utils import timezone
from Fee_calculator.models import Origin
import uuid
import datetime
import random
from urllib.parse import quote
import requests
from rest_framework.exceptions import ValidationError
from datetime import timedelta


class CustomUserManager(UserManager):
    def get_by_natural_key(self, username):
        # Natural key can be either username or email
        return self.get(
            Q(**{self.model.USERNAME_FIELD: username}) |
            Q(email=username)
        )

    
# Create your models here.


# Do I need the image or can be nullable.
class User(AbstractUser):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=255, unique=True)
    image = models.FileField(upload_to='images/users', null=True, blank=True)
    
    verification_token = models.CharField(max_length=255, null=True, blank=True)
    verification_expiry = models.DateTimeField(default=timezone.now() + datetime.timedelta(hours=24), null=True, blank=True)
    is_verified = models.BooleanField(default=False,help_text="True if the user verified the account via email/phone.")
    verification_email_resend_count = models.IntegerField(default=0, help_text="Tracks the number of email verification resends")
    last_verification_email_request = models.DateTimeField(null=True, blank=True)


    # Override first_name and last_name to make them required
    first_name = models.CharField(max_length=150, blank=False, null=False)
    last_name = models.CharField(max_length=150, blank=False, null=False)
    objects = CustomUserManager()

    otp_code = models.CharField(max_length=4, null=True, blank=True, unique=True)
    otp_expiry = models.DateTimeField(null=True, blank=True)

    def generate_otp(self):
        """Generate a unique 4-digit OTP and set its expiry time."""
        otp = str(random.randint(1000, 9999))

        # Ensure OTP is unique across all users
        while User.objects.filter(otp_code=otp).exists():
            otp = str(random.randint(1000, 9999))

    # OTP related fields
    otp_code = models.CharField(max_length=4, null=True, blank=True, unique=True)
    otp_expiry = models.DateTimeField(null=True, blank=True)
    otp_attempts = models.IntegerField(default=0, help_text="Number of OTP attempts made")
    otp_resend_count = models.IntegerField(default=0, help_text="Tracks the number of OTP resends")
    last_otp_request = models.DateTimeField(null=True, blank=True)

    def generate_otp(self):
        """Generate a 4-digit OTP and set an expiry time."""
        otp = str(random.randint(1000, 9999))
        # Ensure OTP is unique across all users
        while User.objects.filter(otp_code=otp).exists():
            otp = str(random.randint(1000, 9999))
        self.otp_code = otp
        self.otp_expiry = timezone.now() + timedelta(minutes=10)
        self.last_otp_request = timezone.now()
        self.otp_attempts = 0  # Reset attempts
        self.save()

    def send_otp_mtn(self):
        """Send OTP via MTN's API."""
        if not self.phone.startswith('+963'):
            raise ValueError("Only Syrian phone numbers (+963) are allowed.")

        # Generate the OTP if it's not already generated
        if not self.otp_code:
            self.generate_otp()

        otp_str = f'Your Verification code is: {self.otp_code}'
        encoded_otp = quote(otp_str)
        url = f'https://services.mtnsyr.com:7443/general/MTNSERVICES/ConcatenatedSender.aspx?User=anem541&Pass=ssor151411&From=Across%20Mena&Gsm={self.phone[1:]}&Msg={encoded_otp}&Lang=0'
        response = requests.get(url)

        if response.status_code != 200:
            raise ValidationError({"otp": "Failed to send OTP via MTN."})

        return response.content

    def can_resend_otp(self):
        """Checks if the OTP can be resent based on the resend count and cooldown period."""
        if self.is_verified:
            return False, "OTP cannot be resent as the phone number is already verified."

        # Define cooldown periods based on resend count
        cooldown_period = 0  # Default for the first attempt
        if self.otp_resend_count == 1:
            cooldown_period = 5  # 5 minutes for the second attempt
        elif self.otp_resend_count >= 2:
            cooldown_period = 60  # 60 minutes for subsequent attempts

        # Check if enough time has passed since the last request
        if self.last_otp_request:
            time_since_last_request = (timezone.now() - self.last_otp_request).total_seconds() / 60
            if time_since_last_request < cooldown_period:
                minutes_left = int(cooldown_period - time_since_last_request)
                return False, f"Please wait for {minutes_left} minutes to resend OTP."
        return True, ""
    

    def request_otp(self):
        """Generate and send a new OTP if the user can request it."""
        can_resend, message = self.can_resend_otp()
        if not can_resend:
            return False, message
        
        self.otp_resend_count += 1
        self.generate_otp()
        self.send_otp_mtn()  # Call send_otp_mtn here to actually send the OTP
        return True, "OTP has been resent successfully."

    def verify_otp(self, otp_input):
        """Verify the OTP and handle expiration or max attempts."""
        if self.is_verified:
            return False, "This phone number is already verified. OTP verification is not required."
        
        if self.otp_expiry and timezone.now() > self.otp_expiry:
            return False, "OTP has expired. Request a new OTP."

        if otp_input != self.otp_code:
            self.otp_attempts += 1
            self.save()
            if self.otp_attempts >= 5:
                return False, "Maximum OTP verification attempts exceeded. Request a new OTP."
            return False, "Invalid OTP."

        # OTP is correct; reset fields and mark as verified
        self.is_verified = True
        self.otp_code = None
        self.otp_expiry = None
        self.otp_attempts = 0
        self.otp_resend_count = 0  # Reset resend count on successful verification
        self.save()
        return True, "OTP verified successfully."

    
    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email  # Generate a unique username

        if self.email:
            self.email = self.email.lower()  # Normalize email to lowercase
        super().save(*args, **kwargs)



class AcrossMenaUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255,default='',blank=True)
    country = models.ForeignKey(Origin,null=True,on_delete=models.SET_NULL)
    
    def __str__(self) :
        return self.user.username