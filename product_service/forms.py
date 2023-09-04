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
            'category', 'excerpt', 'type',
            'slug', 'image', 'image_url', 'author',
        ]

        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'excerpt': forms.Textarea(attrs={'rows': 3}),
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
            'slug': 'Slug',
            'image': 'Image',
            'image_url': 'Image URL',
            'author': 'Author',
        }
