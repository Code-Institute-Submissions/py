import uuid

from django.db import models
from django.db.models import Sum
from django.conf import settings
from django_countries.fields import CountryField

from product_service.models import Product, Service
from homepage.models import UserProfile
from django_plexosoft.settings import (
    NORMAL_DISCOUNT_PERCENTAGE, NORMAL_DISCOUNT_THRESHOLD,
    GRAND_DISCOUNT_PERCENTAGE, GRAND_DISCOUNT_THRESHOLD)

ORDER_STATUS = (
    (0, 'Pending'),
    (1, 'Cancelled'),
    (2, 'Completed'),
)

GATEWAY_TYPE = (
    (0, 'Pending'),
    (1, 'Stripe'),
    (2, 'Manual'),
    (3, 'Crypto'),
)


class Order(models.Model):
    status = models.IntegerField(choices=ORDER_STATUS, default=0)
    order_number = models.CharField(max_length=32, null=False, editable=False)
    buyer_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                                      null=True, blank=True,
                                      related_name='order_instance')
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = CountryField(blank_label='Country *', null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    order_total = models.DecimalField(max_digits=10, decimal_places=2,
                                      null=False, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2,
                                      null=False, default=0)
    stripe_pid = models.CharField(max_length=254, null=False, blank=False,
                                  default='')
    gateway = models.IntegerField(choices=GATEWAY_TYPE, default=0)

    def _generate_order_number(self):
        """
        Generate a random, unique order number using UUID
        """
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        Update grand total each time a line item is added.
        """
        self.order_total = self.lineitems.aggregate(
            Sum('lineitem_total'))['lineitem_total__sum'] or 0
        if self.order_total < settings.GRAND_DISCOUNT_THRESHOLD:
            sdp = settings.NORMAL_DISCOUNT_PERCENTAGE
            normal_discount = self.order_total * sdp / 100
            self.grand_total = self.order_total - normal_discount
        else:
            sdp = settings.GRAND_DISCOUNT_PERCENTAGE
            grand_discount = self.order_total * sdp / 100
            self.grand_total = self.order_total - grand_discount
        self.save()

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already and update the buyer_profile.
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderLineItem(models.Model):
    order = models.ForeignKey(Order, null=False, blank=False,
                              on_delete=models.CASCADE,
                              related_name='lineitems')
    product = models.ForeignKey(Product, null=True, blank=True,
                                on_delete=models.CASCADE)
    service = models.ForeignKey(Service, null=True, blank=True,
                                on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2,
                                         null=False, blank=False,
                                         editable=False)

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the lineitem total
        and update the order total.
        """

        if self.product:
            self.lineitem_total = self.product.price * self.quantity
        elif self.service:
            self.lineitem_total = self.service.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        self.product_instance = self.product
        self.service_instance = self.service

        if self.product_instance:
            return f'SKU {self.product.sku} on order {self.order.order_number}'
        elif self.service_instance:
            return f'SKU {self.service.sku} on order {self.order.order_number}'
