# Django Imports
from django import forms
from django.utils.text import slugify

# Local Imports
from .models import Product, Service, Category

# Product Creation


class AdminProductCreationForm(forms.ModelForm):
    title = forms.CharField(
        required=True, help_text='Insert a descriptive title')
    price = forms.DecimalField(
        required=True, help_text='Insert a fair price for the product')

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Select a Category",
        help_text='Select a proper category for this product'
    )

    def save(self, commit=True):
        instance = super(AdminProductCreationForm, self).save(commit=False)
        instance.slug = slugify(instance.title)
        if commit:
            instance.save()
            instance.code.set(self.cleaned_data['code'])
            instance.service.set(self.cleaned_data['service'])
        else:
            self.save_m2m = lambda: (
                instance.code.set(self.cleaned_data['code']),
                instance.service.set(self.cleaned_data['service']))
        return instance

    class Meta:
        model = Product
        fields = [
            'title', 'sku', 'price', 'description', 'status',
            'category', 'excerpt', 'type', 'code', 'service',
            'preview', 'docs', 'slug', 'image', 'image_url', 'author',
        ]

        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'maxlength': 256}),
            'excerpt': forms.Textarea(attrs={'rows': 3, 'maxlength': 128}),
        }

        labels = {
            'title': 'Title',
            'sku': 'Sku',
            'price': 'Price',
            'description': 'Description',
            'status': 'Status',
            'category': 'Category',
            'excerpt': 'Excerpt',
            'type': 'Type',
            'code': 'Code Type',
            'service': 'Service Type',
            'preview': 'Preview Link',
            'docs': 'Docs Link',
            'image': 'Image',
            'image_url': 'Image URL',
            'author': 'Author',

        }

        help_texts = {
            'sku': 'Insert your unique SKU number',
            'description': 'Insert a clear description of the product',
            'status': 'Select a proper status for this product',
            'excerpt': 'Insert a short excerpt about this product',
            'type': 'Select the type of product',
            'code': 'Hold down “Control”, or “Command” on a Mac, to select more than one.',
            'service': 'Hold down “Control”, or “Command” on a Mac, to select more than one.',
            'preview': 'Insert the preview link of the live product',
            'docs': 'Insert the docs link of the product',
            'image': 'File size cannot exceed 500 KB',
            'image_url': 'Insert an external or local Image URL',
            'author': 'The author has been automatically selected',
        }


class AdminServiceCreationForm(forms.ModelForm):

    title = forms.CharField(
        required=True, help_text='Insert a descriptive title')
    price = forms.DecimalField(
        required=True, help_text='Insert a fair price for the service')

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Select a Category",
        help_text='Select a proper category for this service'
    )

    def save(self, commit=True):
        instance = super(AdminServiceCreationForm, self).save(commit=False)
        instance.slug = slugify(instance.title)
        if commit:
            instance.save()
            instance.code.set(self.cleaned_data['code'])
            instance.service.set(self.cleaned_data['service'])
        else:
            self.save_m2m = lambda: (
                instance.code.set(self.cleaned_data['code']),
                instance.service.set(self.cleaned_data['service']),)
        return instance

    class Meta:
        model = Service
        fields = [
            'title', 'sku', 'price', 'description', 'status',
            'category', 'excerpt', 'type', 'code', 'service',
            'preview', 'docs', 'slug', 'image', 'image_url', 'author',
        ]

        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'maxlength': 256}),
            'excerpt': forms.Textarea(attrs={'rows': 3, 'maxlength': 128}),
        }

        labels = {
            'title': 'Title',
            'sku': 'Sku',
            'price': 'Price',
            'description': 'Description',
            'status': 'Status',
            'category': 'Category',
            'excerpt': 'Excerpt',
            'type': 'Scope Type',
            'code': 'Code Type',
            'service': 'Service Type',
            'preview': 'Preview Link',
            'docs': 'Docs Link',
            'image': 'Image',
            'image_url': 'Image URL',
            'author': 'Author',

        }

        help_texts = {
            'sku': 'Insert your unique SKU number',
            'description': 'Insert a clear description of the service',
            'status': 'Select a proper status for this service',
            'excerpt': 'Insert a short excerpt about this service',
            'type': 'Select the scope type',
            'code': 'Hold down “Control”, or “Command” on a Mac, to select more than one.',
            'service': 'Hold down “Control”, or “Command” on a Mac, to select more than one.',
            'preview': 'Insert the preview link of the live service',
            'docs': 'Insert the docs link of the service',
            'image': 'File size cannot exceed 500 KB',
            'image_url': 'Insert an external or local Image URL',
            'author': 'The author has been automatically selected',
        }
