from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'category', 'image', 'oth_images',
                  'description', 'price', 'gender', 'size', 'color', 'quantity']
        widgets = {
            "title": forms.TextInput(),
        }
