from django import forms
from .models import Region


class RegionForm(forms.ModelForm):
    class Meta:
        model = Region
        fields = ['title', 'federal_district', 'delivery_cost']
        widgets = {
            "title": forms.TextInput(),
            "federal_district": forms.TextInput(),
        }
