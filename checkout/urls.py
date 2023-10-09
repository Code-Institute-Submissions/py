# Django Imports
from django.urls import path, include

# Local Imports
from .views import (Checkout, CheckoutSuccess, CheckoutCancel)
from .stripe import (StripeCheckoutView, StripeCheckoutRedirect)
from .webhooks import StripeWebhookView

urlpatterns = [
    # GENERAL
    path('checkout/', Checkout.as_view(),
         name='checkout_page'),

    # STRIPE
    path('checkout/stripe/form/', StripeCheckoutView.as_view(),
         name='checkout_stripe_form'),
    path('checkout/stripe/redirect/<order_number>',
         StripeCheckoutRedirect.as_view(), name='stripe_redirect'),

    # FEEDBACK
    path('checkout/success/',
         CheckoutSuccess.as_view(), name='checkout_success'),
    path('checkout/cancel/',
         CheckoutCancel.as_view(), name='checkout_cancel'),

    # POST events (Webhook) - Stripe
    path('webhook/', StripeWebhookView.as_view(),
         name='webhook'),
]
