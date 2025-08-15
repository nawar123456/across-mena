
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

        self.otp_code = otp
        self.otp_expiry = timezone.now() + datetime.timedelta(minutes=10)
        self.save()

    def send_otp_mtn(self):
        """Send OTP via MTN's API."""
        if not self.phone.startswith('+963'):
            raise ValueError("Only Syrian phone numbers (+963) are allowed.")

        # Generate the OTP if it's not already generated
        if not self.otp_code:
            self.generate_otp()

        otp_str = 'Your Verification code is: '+str(self.otp_code)
        encoded_otp = quote(otp_str)
        url = f'https://services.mtnsyr.com:7443/general/MTNSERVICES/ConcatenatedSender.aspx?User=anem541&Pass=ssor151411&From=Across%20Mena&Gsm={self.phone[1:]}&Msg={encoded_otp}&Lang=0'
        response = requests.get(url)
        # Check the response from MTN and handle errors if necessary
        if response.status_code != 200:
            raise ValidationError({"otp": "Failed to send OTP via MTN."})

        return response.content

    def verify_otp(self, otp_input):
        """Check if the provided OTP is valid and has not expired. If valid, mark the user as verified."""
        if self.otp_expiry and timezone.now() > self.otp_expiry:
            return False, "OTP has expired."

        if otp_input != self.otp_code:
            return False, "Invalid OTP."

        # OTP is valid, clear the OTP fields and mark the user as verified
        self.otp_code = None
        self.otp_expiry = None
        self.is_verified = True  # Mark user as verified
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

