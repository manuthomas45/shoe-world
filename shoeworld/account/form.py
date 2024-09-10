from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User
import re
from django.core.exceptions import ValidationError



class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'password']

    def clean_email(self):
        email =self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")   
        return email

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return confirm_password
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number:
            phone_number = phone_number.strip() 
            
            if not re.match(r'^\d{10}$', phone_number):
                raise ValidationError("Phone number must be exactly 10 digits.")

        return phone_number
    

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if first_name:
            first_name = first_name.strip() 

            if ' ' in first_name:
                raise ValidationError("First name cannot contain spaces")
            
            if not first_name.isalpha():
                raise ValidationError("First name must contain only letters")
            
            if len(first_name) < 2:
                raise ValidationError("First name must be at least 2 characters long")
            
            if len(first_name) > 20:
                raise ValidationError("First name cannot be longer than 20 characters")
            
        


        return first_name



class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))