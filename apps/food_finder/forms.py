from django import forms
from .models import Restaurant

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'description', 'address', 'city', 'cuisine_type', 'contact_number', 'opening_hours']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Restaurant Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Short description'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Gatuslao Street'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Kabankalan'}),
            'cuisine_type': forms.Select(attrs={'class': 'form-select'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 09123456789'}),
            'opening_hours': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 9:00 AM - 10:00 PM'}),
        }