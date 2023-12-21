from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Account, Buyer, Seller, DeliveryCompany
from django.db import transaction
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render


class BuyerSignUpForm(UserCreationForm):
    password1 = forms.CharField(

        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),

    )
    password2 = forms.CharField(

        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    phone_number = forms.IntegerField(required=True)

    class Meta(UserCreationForm.Meta):
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone_number = self.cleaned_data['phone_number']
        user.is_buyer = True
        user.is_verified = True
        # Set the username based on the first name
        username = self.cleaned_data['email'].lower().split('@')[0]
        user.username = username

        if commit:
            user.save()

            buyer = Buyer.objects.create(user=user)
            buyer.first_name = user.first_name
            buyer.last_name = user.last_name
            buyer.phone_number = user.phone_number
            buyer.save()

        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last Name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'
        self.fields['password1'].widget.attrs['placeholder'] = 'Enter Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def is_valid(self):
        # Override is_valid() method to apply Bootstrap classes to all errors
        valid = super().is_valid()
        if not valid:
            for field in self.errors:
                # Add 'is-invalid' class to field widget
                self[field].field.widget.attrs['class'] += ' is-invalid'
        return valid


class SellerSignUpForm(UserCreationForm):
    buisness_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    #latitude = forms.DecimalField(required=True)
    #longitude = forms.DecimalField(required=True)
    phone_number = forms.IntegerField(required=True)
    merchant_id = forms.CharField(required=True)
    verification_image = forms.ImageField(required=True)

    class Meta(UserCreationForm.Meta):
        model = Account
        fields = ['buisness_name', 'email', 
                   'phone_number', 'merchant_id', 'verification_image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['buisness_name'].widget.attrs['placeholder'] = 'Enter Business Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'
       # self.fields['latitude'].widget.attrs['placeholder'] = 'Enter Latitude'
       # self.fields['longitude'].widget.attrs['placeholder'] = 'Enter Longitude'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
        self.fields['merchant_id'].widget.attrs['placeholder'] = 'Enter Merchant ID'
        self.fields['verification_image'].widget.attrs['placeholder'] = 'Enter Img'

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_seller = True
        user.email = self.cleaned_data.get('email')
        username = self.cleaned_data['email'].lower().split('@')[0]
        user.username = username
        if commit:
            user.save()

            seller = Seller.objects.create(user=user)
            seller.buisness_name = self.cleaned_data.get('buisness_name')
            seller.phone_number = self.cleaned_data.get('phone_number')
            #seller.latitude = self.cleaned_data.get('latitude')
            #seller.longitude = self.cleaned_data.get('longitude')
            seller.merchant_id = self.cleaned_data.get('merchant_id')
            seller.verification_image = self.cleaned_data.get(
                'verification_image')
            seller.save()

        return user

    def is_valid(self):
        # Override is_valid() method to apply Bootstrap classes to all errors
        valid = super().is_valid()
        if not valid:
            for field in self.errors:
                # Add 'is-invalid' class to field widget
                self[field].field.widget.attrs['class'] += ' is-invalid'
        return valid


class DeliverySignUpForm(UserCreationForm):
    company_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    phone_number = forms.IntegerField(required=True)
    delivery_fee = forms.FloatField(required=True)
    verification_image = forms.ImageField(required=True)
    location = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = Account
        fields = ['company_name', 'email', 'phone_number',
                  'delivery_fee', 'verification_image', 'location']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['company_name'].widget.attrs['placeholder'] = 'Enter Business Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
        self.fields['delivery_fee'].widget.attrs['placeholder'] = 'Enter Fee Per Km'
        self.fields['verification_image'].widget.attrs['placeholder'] = 'Enter Img'
        self.fields['location'].widget.attrs['placeholder'] = 'Enter Location'

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_delivery_company = True
        user.email = self.cleaned_data.get('email')
        username = self.cleaned_data['email'].lower().split('@')[0]
        user.username = username
        if commit:
            user.save()

            delivery = DeliveryCompany.objects.create(user=user)
            delivery.company_name = self.cleaned_data.get('company_name')
            delivery.phone_number = self.cleaned_data.get('phone_number')
            delivery.delivery_fee = self.cleaned_data.get('delivery_fee')
            delivery.location = self.cleaned_data.get('location')
            delivery.verification_image = self.cleaned_data.get(
                'verification_image')
            delivery.save()

        return user

    def is_valid(self):
        # Override is_valid() method to apply Bootstrap classes to all errors
        valid = super().is_valid()
        if not valid:
            for field in self.errors:
                # Add 'is-invalid' class to field widget
                self[field].field.widget.attrs['class'] += ' is-invalid'
        return valid
