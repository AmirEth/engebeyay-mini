from django.db import models
from accounts.models import Account
# Create your models here.


class Company_Information(models.Model):
    company_name = models.CharField(max_length=50)
    current_admin = models.OneToOneField(
        Account, on_delete=models.SET_NULL, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    contact_phone = models.CharField(max_length=15)
    contact_email = models.EmailField(max_length=200, unique=True)
    deployment_date = models.DateField(null=True)

    def __str__(self):
        return self.company_name


class Payment_Method(models.Model):
    payment_method = models.CharField(max_length=100)
    payment_provider = models.CharField(max_length=100)
    currency = models.CharField(max_length=100)
    merchant_id = models.CharField(max_length=100)
    included_date = models.DateField(null=True, auto_now_add=True)
    reverse_url= models.CharField(max_length=250,null=True)

    def __str__(self):
        return self.payment_method


class Message(models.Model):
    message_id = models.AutoField(primary_key=True)
    message_type = models.CharField(max_length=20, default="feedback")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20)

    def __str__(self):
        return f"Message {self.message_id}"
