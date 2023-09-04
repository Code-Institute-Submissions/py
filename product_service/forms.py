# Django Imports
from django import forms
from django.utils.text import slugify

# Local Imports
from .models import Product

# Product Creation


class AdminProductCreationForm(forms.ModelForm):

    def save(self, commit=True):
        instance = super(AdminProductCreationForm, self).save(commit=False)
        instance.slug = slugify(instance.title)
        if commit:
            instance.save()
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
            'slug': 'Slug',
            'image': 'Image',
            'image_url': 'Image URL',
            'author': 'Author',

        }

        help_texts = {
            'title': 'Title',
            'sku': 'Sku',
            'price': 'Price',
            'description': 'Description',
            'status': 'Status',
            'category': 'Category',
            'excerpt': 'Excerpt',
            'type': 'Type',
            'code': 'Hold down “Control”, or “Command” on a Mac, to select more than one.',
            'service': 'Hold down “Control”, or “Command” on a Mac, to select more than one.',
            'preview': 'Preview Link',
            'docs': 'Docs Link',
            'slug': 'Slug',
            'image': 'File size cannot exceed 500 KB',
            'image_url': 'Image URL',
            'author': 'Author',
        }
