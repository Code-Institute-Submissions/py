# Django Imports
from django import forms

# Local Imports
from product_service.models import Download, Product, Service

# Download Creation


class AdminDownloadCreationForm(forms.ModelForm):
    file_name = forms.CharField(
        required=True, help_text='Insert a descriptive & short file name')

    service = forms.ModelChoiceField(
        queryset=Service.objects.all(),
        required=False,
        help_text='Select a proper service for the file'
    )

    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        required=False,
        help_text='Select a proper product for the file'
    )

    def save(self, commit=True):
        instance = super(AdminDownloadCreationForm, self).save(commit=False)
        if commit:
            instance.save()
        return instance

    class Meta:
        model = Download
        fields = [
            'file_name', 'product', 'service', 'file', 'status',
        ]

        labels = {
            'file_name': 'File Name',
            'product': 'Product Instance',
            'service': 'Service Instance',
            'file': 'File',
            'status': 'Status',
        }

        help_texts = {
            'product': 'Select a proper product for the file',
            'service': 'Select a proper service for the file',
            'file': 'File size cannot exceed 500 MB',
        }
