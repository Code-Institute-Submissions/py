from django.db import models
from django.contrib.auth.models import AbstractUser

ROLES = (
    (0, 'buyer'),
    (1, 'admin'),
)

USER_TYPE = (
    (0, 'individual'),
    (1, 'busisess'),
    (2, 'developer'),
)

STATUS = (
    (0, 'draft'),
    (1, 'suspended'),
    (2, 'active'),
)


class UserProfile(AbstractUser):
    """Extended user profile with custom attributes."""
    role = models.IntegerField(choices=ROLES, default=0)
    type = models.IntegerField(choices=USER_TYPE, default=0)
    status = models.IntegerField(choices=STATUS, default=2)
    user_transactions = models.ManyToManyField(
        'product_service.Product',
        through='product_service.Transaction',
        related_name='user_profiles')


class Comment(models.Model):
    writer = models.ForeignKey(UserProfile, on_delete=models.CASCADE,
                               related_name='user_comments')
    comment = models.TextField(max_length=256, unique=True)
    product = models.ForeignKey('product_service.Product', on_delete=models.CASCADE,
                                related_name='commented_products',
                                null=True, blank=True)
    service = models.ForeignKey('product_service.Service', on_delete=models.CASCADE,
                                related_name='comment_services',
                                null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
    liker = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name='user_likes')
    product = models.ForeignKey('product_service.Product', on_delete=models.CASCADE,
                                related_name='liked_products',
                                null=True, blank=True)
    service = models.ForeignKey('product_service.Service', on_delete=models.CASCADE,
                                related_name='liked_services',
                                null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)


class NewsLetter(models.Model):
    email = models.EmailField(unique=True)
    excerpt = models.CharField(max_length=128)
    created_on = models.DateTimeField(auto_now_add=True)
