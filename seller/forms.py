from django import forms
from  store.models import  Product



class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude=['owner','product_id']