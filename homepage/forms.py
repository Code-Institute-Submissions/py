# Django Imports
from django import forms
from django.utils.text import slugify

# Python imports
from datetime import date

from allauth.account.forms import LoginForm, SignupForm

# Local Imports

from .models import UserProfile


class CustomSignupForm(SignupForm, forms.ModelForm):
    first_name = forms.CharField(
        max_length=30, label='First Name', required=True)
    last_name = forms.CharField(
        max_length=30, label='Last Name', required=True)

    def save(self, request, commit=True):
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.type = self.cleaned_data['type']
        if commit:
            user.save()
        return user

    class Meta:
        model = UserProfile
        fields = [
            'type'
        ]

        labels = {
            'type': 'Account Type',

        }

        help_texts = {
            'type': 'Select Account Type',
        }


CustomLoginForm = LoginForm
