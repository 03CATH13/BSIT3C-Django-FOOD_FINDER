from django import forms
from .models import Restaurant
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# --- ITO YUNG EXISTING FORM MO PARA SA RESTAURANT ---
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


# --- ITO YUNG BAGONG FORM PARA SA SIGN UP (REGISTER) ---
class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'})
    )
    
    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        # Nilalagyan natin ng Bootstrap classes at placeholder ang mga fields
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})