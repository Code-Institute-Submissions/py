from django.db import models

PRODUCT_TYPE(
    (0, 'pending')
    (1, 'ownership'),
    (2, 'license'),
)


class Category(models.Model):
    '''Category model for Product & Service models'''
    category_name = models.CharField(max_length=64, unique=True)
    alt_name = models.CharField(max_length=64, unique=True)


class Product(models.Model):
    '''Product model for product instances, independent from Service model'''

    # Primary Data
    title = models.CharField(max_length=64, unique=True)
    sku = models.CharField(max_length=64, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(max_length=256)
    status = models.IntegerField(choices=homepage.STATUS, default=0)

    # Secondary Data
    category = models.ForeignKey(
        Category, related_name='product_categories', null=True, blank=True)
    excerpt = models.CharField(max_length=128)
    type = models.IntegerField(choices=PRODUCT_TYPE, default=1)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)

    # Metadata and ManyToManyField Relationship
    author = models.ForeignKey(
        'homepage.UserProfile', on_delete=models.CASCADE,
        related_name='product_authors')
    created_on = models.DateField(auto_now_add=True)
    likes = models.ManyToManyField(
        'homepage.Like', related_name='product_likes', blank=True)
    comments = models.ManyToManyField(
        'homepage.Comment', related_name='product_comments', blank=True)
    transactions = models.ManyToManyField(
        'homepage.UserProfile', through='Transaction',
        related_name='user_profiles', blank=True)

    # Download Feature
    download_url = models.ManyToManyField(
        'Download', related_name='product_downloads', blank=True)


class Service(models.Model):
    '''Service model for service instances, independent from Product model'''

    # Primary Data
    title = models.CharField(max_length=64, unique=True)
    sku = models.CharField(max_length=64, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(max_length=256)
    status = models.IntegerField(choices=homepage.STATUS, default=0)

    # Secondary Data
    category = models.ForeignKey(
        Category, related_name='product_categories', null=True, blank=True)
    excerpt = models.CharField(max_length=128)
    type = models.IntegerField(choices=PRODUCT_TYPE, default=1)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)

    # Metadata and ManyToManyField Relationship
    author = models.ForeignKey(
        'homepage.UserProfile', on_delete=models.CASCADE,
        related_name='product_authors')
    created_on = models.DateField(auto_now_add=True)
    likes = models.ManyToManyField(
        'homepage.Like', related_name='product_likes', blank=True)
    comments = models.ManyToManyField(
        'homepage.Comment', related_name='product_comments', blank=True)
    transactions = models.ManyToManyField(
        'homepage.UserProfile', through='Transaction',
        related_name='user_profiles', blank=True)

    # Download Feature
    download_url = models.ManyToManyField(
        'Download', related_name='product_downloads', blank=True)


class Download(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, blank=True)
    service = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, blank=True)
    file_url = models.URLField(max_length=1024, null=True, blank=True)
    status = models.IntegerField(choices=homepage.STATUS, default=0)


class Transaction(models.Model):
    buyer = models
    product = models
    service = models
    sku = models
    price = models
    paid = models
    item_url = models
    gateway = models
    timestamp = models