from django.db import models

from homepage.models import STATUS

ITEM_TYPE = (
    (0, 'Pending'),
    (1, 'Ownership'),
    (2, 'License'),
)

GATEWAY_TYPE = (
    (0, 'Pending'),
    (1, 'Stripe'),
    (2, 'Manual'),
    (3, 'Crypto'),
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

    description = models.TextField(max_length=256)

    status = models.IntegerField(choices=STATUS, default=0)

    # Secondary Data
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name='product_categories', null=True, blank=True)

    excerpt = models.CharField(max_length=128)

    type = models.IntegerField(choices=ITEM_TYPE, default=1)

    code = models.ManyToManyField(CodeType, related_name="code_type")

    service = models.ManyToManyField(ServiceType, related_name="service_type")

    preview = models.URLField(
        max_length=1024, null=True, blank=True, unique=True)

    docs = models.URLField(
        max_length=1024, null=True, blank=True, unique=True)

    slug = models.SlugField(max_length=200, unique=True)

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

    transactions = models.ManyToManyField(
        'homepage.UserProfile', through='Transaction',
        related_name='product_transactions', blank=True)

    # Download Feature
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

    description = models.TextField(max_length=256)

    status = models.IntegerField(choices=STATUS, default=0)

    # Secondary Data
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name='service_categories', null=True, blank=True)

    excerpt = models.CharField(max_length=128)

    type = models.IntegerField(choices=ITEM_TYPE, default=1)

    slug = models.SlugField(max_length=200, unique=True)

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

    transactions = models.ManyToManyField(
        'homepage.UserProfile', through='Transaction',
        related_name='service_transactions', blank=True)

    # Download Feature
    download_url = models.ManyToManyField(
        'Download', related_name='service_downloads', blank=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Download(models.Model):
    product = models.ForeignKey(
        Product, related_name='product_downloads',
        on_delete=models.SET_NULL, null=True, blank=True)

    service = models.ForeignKey(
        Service, related_name='service_downloads',
        on_delete=models.SET_NULL, null=True, blank=True)

    file_url = models.URLField(max_length=1024, null=True, blank=True)

    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ['product', 'service']

    def __str__(self):
        return f'{self.file_url}'


class Transaction(models.Model):
    buyer = models.ForeignKey('homepage.UserProfile',
                              on_delete=models.SET_NULL,
                              related_name='buyer_transactions',
                              null=True)

    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, blank=True)

    service = models.ForeignKey(
        Service, on_delete=models.SET_NULL, null=True, blank=True)

    sku = models.CharField(max_length=64, null=True, blank=True)

    price = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)

    paid = models.DecimalField(max_digits=6, decimal_places=2)

    item_url = models.URLField(max_length=1024, null=True, blank=True)

    gateway = models.IntegerField(choices=GATEWAY_TYPE, default=0)

    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.product:
            self.sku = self.product.sku
            self.price = self.product.price
            download_urls = self.product.download_url.all()
            if download_urls.exists():
                self.item_url = download_urls.first().file_url
        elif self.service:
            self.sku = self.service.sku
            self.price = self.service.price
            download_urls = self.service.download_url.all()
            if download_urls.exists():
                self.item_url = download_urls.first().file_url
        super(Transaction, self).save(*args, **kwargs)

    class Meta:
        ordering = ['product', 'service']

    def __str__(self):
        return f'{self.buyer.username}'
