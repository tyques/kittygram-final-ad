import re
from django import forms
from django.db import models
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    """Form for user registration."""
    
    name = forms.CharField(max_length=124, required=True, label='Name')
    surname = forms.CharField(max_length=124, required=True, label='Surname')
    email = forms.EmailField(required=True, label='Email')
    phone = forms.CharField(max_length=12, required=True, label='Phone')
    
    class Meta:
        model = User
        fields = ('name', 'surname', 'email', 'phone', 'password1', 'password2')
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        
        # Validate phone format: 8XXXXXXXXXX or +7XXXXXXXXXX
        pattern = r'^(\+7|8)\d{10}$'
        if not re.match(pattern, phone):
            raise ValidationError('Phone number must be in format 8XXXXXXXXXX or +7XXXXXXXXXX')
        
        # Normalize phone to +7 format for uniqueness check
        normalized_phone = '+7' + phone[1:] if phone.startswith('8') else phone
        
        # Check for uniqueness (considering both formats)
        existing_users = User.objects.filter(
            models.Q(phone=normalized_phone) | 
            models.Q(phone='8' + normalized_phone[2:])
        )
        if self.instance.pk:
            existing_users = existing_users.exclude(pk=self.instance.pk)
        
        if existing_users.exists():
            raise ValidationError('This phone number is already in use')
        
        return normalized_phone


class UserLoginForm(AuthenticationForm):
    """Form for user login."""
    
    username = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')


class UserProfileForm(forms.ModelForm):
    """Form for editing user profile."""
    
    class Meta:
        model = User
        fields = ('name', 'surname', 'avatar', 'about', 'phone', 'github_url')
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        
        # Validate phone format: 8XXXXXXXXXX or +7XXXXXXXXXX
        pattern = r'^(\+7|8)\d{10}$'
        if not re.match(pattern, phone):
            raise ValidationError('Phone number must be in format 8XXXXXXXXXX or +7XXXXXXXXXX')
        
        # Normalize phone to +7 format for uniqueness check
        normalized_phone = '+7' + phone[1:] if phone.startswith('8') else phone
        
        # Check for uniqueness (considering both formats)
        existing_users = User.objects.filter(
            models.Q(phone=normalized_phone) | 
            models.Q(phone='8' + normalized_phone[2:])
        )
        if self.instance.pk:
            existing_users = existing_users.exclude(pk=self.instance.pk)
        
        if existing_users.exists():
            raise ValidationError('This phone number is already in use')
        
        return normalized_phone
    
    def clean_github_url(self):
        github_url = self.cleaned_data.get('github_url')
        if github_url:
            # Validate that it's a GitHub URL
            if 'github.com' not in github_url:
                raise ValidationError('URL must be a valid GitHub URL')
        return github_url


class CustomPasswordChangeForm(PasswordChangeForm):
    """Custom password change form."""
    
    old_password = forms.CharField(widget=forms.PasswordInput, label='Old password')
    new_password1 = forms.CharField(widget=forms.PasswordInput, label='New password')
    new_password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm new password')
