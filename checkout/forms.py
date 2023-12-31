from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('full_name', 'country', 'email', 'phone_number', 'gateway',)

    def __init__(self, request, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field and pass
        the request.
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'gateway': 'Gateway',
        }
        if request.user.is_authenticated:
            self.fields['full_name'].widget.attrs[
                'value'] = request.user.first_name + ' ' + \
                request.user.last_name
            self.fields['email'].widget.attrs['value'] = request.user.email

        self.fields['full_name'].widget.attrs['autofocus'] = True

        for field in self.fields:
            if field != 'country':

                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]

                self.fields[field].widget.attrs['placeholder'] = placeholder

            self.fields[field].widget.attrs['class'] = 'mt-2'
            self.fields[field].label = False
