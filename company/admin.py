from django.contrib import admin
from .models import Payment_Method, Message, Company_Information
# Register your models here.

admin.site.register(Company_Information)
admin.site.register(Payment_Method)
admin.site.register(Message)
