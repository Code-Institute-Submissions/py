# Django Imports
from django.urls import path, include

# Local Imports
from .views import (Checkout, CheckoutSuccess, CacheCheckoutDataView)
from .stripe import StripeCheckoutView
from .webhooks import StripeWebhookView

urlpatterns = [

    path('checkout/', Checkout.as_view(),
         name='checkout_page'),
    path('checkout/success/<order_number>', CheckoutSuccess.as_view(),
         name='checkout_success'),
    path('checkout/stripe/form/', StripeCheckoutView.as_view(),
         name='checkout_stripe_form'),
    path('webhook/', StripeWebhookView.as_view(),
         name='webhook'),
    path('cache_checkout/', CacheCheckoutDataView.as_view(),
         name='cache_checkout'),
]
