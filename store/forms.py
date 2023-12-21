from django import forms
from .models import ReviewRating, Product
class ProductAddForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude=['owner',]

class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['subject', 'review', 'rating']
        


