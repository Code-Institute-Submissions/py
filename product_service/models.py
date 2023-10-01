from django.db import models
import uuid
from homepage.models import STATUS
from django.utils import timezone
import os
from .utils import generate_download_token

SCOPE_TYPE = (
    (0, 'NA'),
    (1, 'Ownership'),
    (2, 'License'),
)

GATEWAY_TYPE = (
    (0, 'Pending'),
    (1, 'Stripe'),
    (2, 'Manual'),
    (3, 'Crypto'),
)

INSTANCE_TYPE = (
    (0, 'Product'),
    (1, 'Service'),
)


class CodeType(models.Model):
    code = models.CharField(max_length=64, unique=True)

    class Meta:
        ordering = ['code']
        verbose_name_plural = "CodeTypes"

    def __str__(self):
        return self.code


class ServiceType(models.Model):
    service = models.CharField(max_length=64, unique=True)

    class Meta:
        ordering = ['service']
        verbose_name_plural = "ServiceTypes"

    def __str__(self):
        return self.service


class Category(models.Model):
    '''Category model for Product & Service models'''
    category_name = models.CharField(max_length=64, unique=True)

    alt_name = models.CharField(max_length=64, unique=True)

    class Meta:
        ordering = ['category_name']
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category_name


class Product(models.Model):
    '''Product model for product instances, independent from Service model'''

    # Primary Data
    title = models.CharField(max_length=64, unique=True)

    sku = models.CharField(max_length=64, unique=True)

    price = models.DecimalField(max_digits=6, decimal_places=2)

    description = models.TextField(max_length=528)

    status = models.IntegerField(choices=STATUS, default=0)

    # Secondary Data
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name='product_categories', null=True, blank=True)

    excerpt = models.CharField(max_length=264)

    type = models.IntegerField(choices=SCOPE_TYPE, default=1)

    instance = models.IntegerField(choices=INSTANCE_TYPE, default=0)

    code = models.ManyToManyField(CodeType, related_name="code_type")

    service = models.ManyToManyField(ServiceType, related_name="service_type")

    preview = models.URLField(
        max_length=1024, null=True, blank=True, unique=True)

    docs = models.URLField(
        max_length=1024, null=True, blank=True, unique=True)

    slug = models.SlugField(max_length=200, unique=True, blank=True)

    image = models.ImageField(null=True, blank=True)

    image_url = models.URLField(max_length=1024, null=True, blank=True)

    # Metadata and ManyToManyField Relationship
    author = models.ForeignKey(
        'homepage.UserProfile', on_delete=models.SET_NULL,
        related_name='product_authors', null=True)

    created_on = models.DateTimeField(auto_now_add=True)

    likes = models.ManyToManyField(
        'homepage.Like', related_name='product_likes', blank=True)

    comments = models.ManyToManyField(
        'homepage.Comment', related_name='product_comments', blank=True)

    orders = models.ManyToManyField(
        'checkout.Order', related_name='product_orders', blank=True)

    # Download Data
    download_url = models.ManyToManyField(
        'Download', related_name='product_downloads', blank=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Service(models.Model):
    '''Service model for service instances, independent from Product model'''

    # Primary Data
    title = models.CharField(max_length=64, unique=True)

    sku = models.CharField(max_length=64, unique=True)

    price = models.DecimalField(max_digits=6, decimal_places=2)

    description = models.TextField(max_length=528)

    status = models.IntegerField(choices=STATUS, default=0)

    # Secondary Data
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name='service_categories', null=True, blank=True)

    excerpt = models.CharField(max_length=264)

    type = models.IntegerField(choices=SCOPE_TYPE, default=1)

    instance = models.IntegerField(choices=INSTANCE_TYPE, default=1)

    code = models.ManyToManyField(CodeType, related_name="code_type_service")

    service = models.ManyToManyField(
        ServiceType, related_name="on_service_type")

    preview = models.URLField(
        max_length=1024, null=True, blank=True, unique=True)

    docs = models.URLField(
        max_length=1024, null=True, blank=True, unique=True)

    slug = models.SlugField(max_length=200, unique=True, blank=True)

    image = models.ImageField(null=True, blank=True)

    image_url = models.URLField(max_length=1024, null=True, blank=True)

    # Metadata and ManyToManyField Relationship
    author = models.ForeignKey(
        'homepage.UserProfile', on_delete=models.SET_NULL,
        related_name='service_authors', null=True)

    created_on = models.DateTimeField(auto_now_add=True)

    likes = models.ManyToManyField(
        'homepage.Like', related_name='service_likes', blank=True)

    comments = models.ManyToManyField(
        'homepage.Comment', related_name='service_comments', blank=True)

    # Download Data
    download_url = models.ManyToManyField(
        'Download', related_name='service_downloads', blank=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


def custom_upload_to(instance, filename):
    """
    Generates a unique filename based on the instance's token.
    """
    ext = filename.split('.')[-1]
    return os.path.join('downloads', f'{instance.token}.{ext}')


class Download(models.Model):
    file_name = models.CharField(
        max_length=64, unique=True, null=True, blank=True)
    product = models.ForeignKey(
        Product, related_name='product_downloads',
        on_delete=models.SET_NULL, null=True, blank=True)

    service = models.ForeignKey(
        Service, related_name='service_downloads',
        on_delete=models.SET_NULL, null=True, blank=True)

    file = models.FileField(upload_to=custom_upload_to, null=True, blank=True)

    status = models.IntegerField(choices=STATUS, default=0)

    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    download_token = models.CharField(max_length=12, unique=True)

    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['product', 'service']

    @property
    def file_url(self):
        if self.file:
            # Assuming you want to generate a URL based on the current host
            # You can change this logic if you have a specific host in mind
            return self.file.url
        return None

    def _generate_download_token(self):
        return generate_download_token()

    def save(self, *args, **kwargs):
        if not self.download_token:
            self.download_token = self._generate_download_token()

        super().save(*args, **kwargs)

    def is_valid(self):
        # Define your logic for token validity here (e.g., expiration time)
        expiration_time = timezone.now() - timezone.timedelta(hours=1)
        return self.created_on >= expiration_time

    def __str__(self):
        return f'{self.file_name}'


# class Transaction(models.Model):
#     buyer = models.ForeignKey('homepage.UserProfile',
#                               on_delete=models.SET_NULL,
#                               related_name='buyer_transactions',
#                               null=True)

#     product = models.ForeignKey(
#         Product, on_delete=models.SET_NULL, null=True, blank=True)

#     service = models.ForeignKey(
#         Service, on_delete=models.SET_NULL, null=True, blank=True)

#     sku = models.CharField(max_length=64, null=True, blank=True)

#     price = models.DecimalField(
#         max_digits=6, decimal_places=2, null=True, blank=True)

#     paid = models.DecimalField(max_digits=6, decimal_places=2)

#     item_url = models.URLField(max_length=1024, null=True, blank=True)

#     gateway = models.IntegerField(choices=GATEWAY_TYPE, default=0)

#     timestamp = models.DateTimeField(auto_now_add=True)

#     def save(self, *args, **kwargs):
#         if self.product:
#             self.sku = self.product.sku
#             self.price = self.product.price
#             download_urls = self.product.download_url.all()
#             if download_urls.exists():
#                 self.item_url = download_urls.first().file_url
#         elif self.service:
#             self.sku = self.service.sku
#             self.price = self.service.price
#             download_urls = self.service.download_url.all()
#             if download_urls.exists():
#                 self.item_url = download_urls.first().file_url
#         super(Transaction, self).save(*args, **kwargs)

#     class Meta:
#         ordering = ['product', 'service']

#     def __str__(self):
#         return f'{self.buyer.username}'
