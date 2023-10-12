from django.db import models
from django.contrib.auth.models import AbstractUser

ROLES = (
    (0, 'Buyer'),
    (1, 'Admin'),
)

USER_TYPE = (
    (0, 'Individual'),
    (1, 'Business'),
    (2, 'Developer'),
)

STATUS = (
    (0, 'Draft'),
    (1, 'Suspended'),
    (2, 'Active'),
)

INSTANCE_TYPE = (
    (0, 'Product'),
    (1, 'Service'),
)


class UserProfile(AbstractUser):
    """Extended user profile with custom attributes."""
    email = models.EmailField(
        unique=True)
    role = models.IntegerField(choices=ROLES, default=0)
    type = models.IntegerField(choices=USER_TYPE, default=0)
    status = models.IntegerField(choices=STATUS, default=2)

    class Meta:
        ordering = ['username']

    def __str__(self):
        return f'{self.username}'


class Comment(models.Model):
    writer = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                               related_name='user_comments',
                               null=True, blank=True)

    comment = models.TextField(max_length=256, unique=True)

    product = models.ForeignKey('product_service.Product',
                                on_delete=models.SET_NULL,
                                related_name='commented_products',
                                null=True, blank=True)

    service = models.ForeignKey('product_service.Service',
                                on_delete=models.SET_NULL,
                                related_name='comment_services',
                                null=True, blank=True)

    status = models.IntegerField(choices=STATUS, default=0)

    instance = models.IntegerField(choices=INSTANCE_TYPE, default=0)

    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f'Commented by {self.writer.username}'


class Like(models.Model):
    liker = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                              related_name='user_likes',
                              null=True, blank=True)

    product = models.ForeignKey('product_service.Product',
                                on_delete=models.SET_NULL,
                                related_name='liked_products',
                                null=True, blank=True)

    service = models.ForeignKey('product_service.Service',
                                on_delete=models.SET_NULL,
                                related_name='liked_services',
                                null=True, blank=True)

    status = models.IntegerField(choices=STATUS, default=0)

    instance = models.IntegerField(choices=INSTANCE_TYPE, default=0)

    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f'Liked by {self.liker.username}'


class NewsLetter(models.Model):
    email = models.EmailField(unique=True)
    excerpt = models.CharField(max_length=128)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']
        verbose_name_plural = "Newsletters"

    def __str__(self):
        return f'{self.email}'
