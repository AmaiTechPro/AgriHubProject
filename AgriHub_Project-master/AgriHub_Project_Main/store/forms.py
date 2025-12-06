from django.contrib.auth import password_validation
from store.models import Address
from django import forms
import django
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.db import models
from django.db.models import fields
from django.forms import widgets
from django.forms.fields import CharField
from django.utils.translation import gettext, gettext_lazy as _



class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Confirm Password'}))
    email = forms.CharField(required=True, widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {'email': 'Email'}
        widgets = {'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Username'})}


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    password = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'class':'form-control'}))


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['locality', 'city', 'state']
        widgets = {'locality':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Popular Place like Restaurant, Religious Site, etc.'}), 'city':forms.TextInput(attrs={'class':'form-control', 'placeholder':'City'}), 'state':forms.TextInput(attrs={'class':'form-control', 'placeholder':'State or Province'})}


class PasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label=_("Old Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'auto-focus':True, 'class':'form-control', 'placeholder':'Current Password'}))
    new_password1 = forms.CharField(label=_("New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password', 'class':'form-control', 'placeholder':'New Password'}), help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_("Confirm Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password', 'class':'form-control', 'placeholder':'Confirm Password'}))


class PasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=_("Email"), max_length=254, widget=forms.EmailInput(attrs={'autocomplete':'email', 'class':'form-control'}))


class SetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label=_("New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password', 'class':'form-control'}), help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_("Confirm Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}))






# In store/forms.py, ADD THIS CODE BLOCK:

from django import forms
from .models import Product # Import the Product model (Produce Item)

class FarmerProductForm(forms.ModelForm):
    # This form is used by the front-end dashboard for farmers
    class Meta:
        model = Product
        fields = [
            'title', 'slug', 'batch_id', 'origin', 
            'produce_details', 'product_image', 'price_per_unit', 
            'unit_type', 'harvest_date', 'category', 
            'is_active', 'is_featured'
        ]
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'batch_id': forms.TextInput(attrs={'class': 'form-control'}),
            'origin': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'produce_details': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'product_image': forms.FileInput(attrs={'class': 'form-control'}),
            'price_per_unit': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'harvest_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }



        # In store/forms.py, ADD THIS CODE BLOCK:

from .models import Address # Import the Address model

class AddressForm(forms.ModelForm):
    # This form handles adding or editing a delivery address
    class Meta:
        model = Address
        # Use only the non-Foreign Key fields visible to the user
        fields = ['locality', 'city', 'state'] 
        
        widgets = {
            'locality': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nearest Location / Area'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City / Town'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'County'}),
        }