from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class Account(AbstractUser):
    email = models.EmailField(max_length=200, unique=True)
    first_name = None
    last_name = None

    is_seller = models.BooleanField('is seller', default=False)
    is_buyer = models.BooleanField('is buyer', default=False)
    last_login = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_delivery_guy = models.BooleanField(default=False)
    is_delivery_company = models.BooleanField(default=False)

    is_verified = models.BooleanField('is verified', default=False)

    is_staff = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_active

    def has_module_perms(self, add_label):
        return True


class Buyer(models.Model):
    user = models.OneToOneField(
        Account, on_delete=models.CASCADE, primary_key=True)

    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    phone_number = models.IntegerField(null=True, blank=True,)

    profile_image = models.ImageField(
        null=True, blank=True, upload_to='profile/buyer/', default='profile/buyer/user-default.png')

    def __str__(self):
        return self.user.email


class Seller(models.Model):
    user = models.OneToOneField(
        Account, on_delete=models.CASCADE, primary_key=True)
    buisness_name = models.CharField(max_length=100, null=True)
    phone_number = models.IntegerField(null=True, blank=True)
 
 #   latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
  #  longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    
    merchant_id = models.CharField(max_length=100, null=True)
    verification_image = models.ImageField(
        null=True, blank=True, upload_to='profile/seller/')

    def __str__(self):
        return self.user.email


class Staff(models.Model):
    user = models.OneToOneField(
        Account, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    phone_number = models.IntegerField(null=True, blank=True)

    profile_image = models.ImageField(
        null=True, blank=True, upload_to='profile/seller/', default='profile/buyer/user-default.png')

    def __str__(self):
        return self.user.email


class DeliveryCompany(models.Model):
    user = models.OneToOneField(
        Account, on_delete=models.CASCADE, primary_key=True)
    company_name = models.CharField(max_length=100, null=True)
    phone_number = models.IntegerField(null=True, blank=True)
    delivery_fee = models.FloatField(null=True, blank=True, default=0,)
    verification_image = models.ImageField(
        null=True, blank=True, upload_to='profile/seller/', default='profile/buyer/user-default.png')
    location = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.user.email


class DeliveryGuy(models.Model):
    user = models.OneToOneField(
        Account, on_delete=models.CASCADE, primary_key=True)
    company = models.ForeignKey(
        DeliveryCompany, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    phone_number = models.IntegerField(null=True, blank=True)
    earnings = models.FloatField(null=True, blank=True, default=0,)
    driven = models.FloatField(null=True, blank=True, default=0,)
    completed_jobs = models.IntegerField(max_length=100, null=True, default=0,)
    status = models.CharField(max_length=100, default="Active")

    def __str__(self):
        return self.user.email
