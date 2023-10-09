# Django Imports
from django import forms
from django.utils.text import slugify
from django.core.validators import MaxLengthValidator

# Python imports
from datetime import date

from allauth.account.forms import LoginForm, SignupForm

# Local Imports

from .models import UserProfile, USER_TYPE, Comment


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(
        max_length=30, label='First Name', required=True)
    last_name = forms.CharField(
        max_length=30, label='Last Name', required=True)
    type = forms.ChoiceField(choices=USER_TYPE, label='Account Type')

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.type = self.cleaned_data['type']
        user.save()
        return user


CustomLoginForm = LoginForm

# Comment creation


class ProductCommentCreationForm(forms.ModelForm):
    comment = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 50}),
        validators=[MaxLengthValidator(256)],
        max_length=256,
    )

    class Meta:
        model = Comment
        fields = ['writer', 'comment', 'product',]


class ServiceCommentCreationForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['writer', 'comment', 'service', 'instance']
