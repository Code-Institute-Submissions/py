# Django Imports
from django import forms
from django.core.validators import MaxLengthValidator

# Python imports

from allauth.account.forms import LoginForm, SignupForm

# Local Imports

from .models import USER_TYPE, Comment


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
    """
    Service form for service instances
    """
    comment = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 50}),
        validators=[MaxLengthValidator(256)],
        max_length=256,
    )

    class Meta:
        model = Comment
        fields = ['comment',]

    def __init__(self, request, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field and pass
        the request.
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'comment': 'Add a ramarkable comment',
        }
        for field in self.fields:
            if field:

                if self.fields[field].required:
                    placeholder = f'{placeholders[field]}'

                self.fields[field].widget.attrs['placeholder'] = placeholder

            self.fields[field].widget.attrs['class'] = 'mb-2'
            self.fields[field].label = False


class ServiceCommentCreationForm(forms.ModelForm):
    """
    Service form for service instances
    """
    comment = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 50}),
        validators=[MaxLengthValidator(256)],
        max_length=256,
    )

    class Meta:
        model = Comment
        fields = ['comment',]

    def __init__(self, request, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field and pass
        the request.
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'comment': 'Add a ramarkable comment',
        }
        for field in self.fields:
            if field:

                if self.fields[field].required:
                    placeholder = f'{placeholders[field]}'

                self.fields[field].widget.attrs['placeholder'] = placeholder

            self.fields[field].widget.attrs['class'] = 'mb-2'
            self.fields[field].label = False


CustomLoginForm = LoginForm
