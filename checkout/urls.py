# Django Imports
from django.urls import path, include

# Local Imports
from .views import (Checkout, CheckoutSuccess, CheckoutCancel)
from .stripe import (StripeCheckoutView, StripeCheckoutRedirect)
from .webhooks import StripeWebhookView

urlpatterns = [

    path('checkout/', Checkout.as_view(),
         name='checkout_page'),
    path('checkout/stripe/form/', StripeCheckoutView.as_view(),
         name='checkout_stripe_form'),
    path('checkout/stripe/redirect/<order_number>',
         StripeCheckoutRedirect.as_view(), name='stripe_redirect'),
    path('checkout/success/',
         CheckoutSuccess.as_view(), name='checkout_success'),
    path('checkout/cancel/',
         CheckoutCancel.as_view(), name='checkout_cancel'),
    # For Stripe to post events (Webhook)
    path('webhook/', StripeWebhookView.as_view(),
         name='webhook'),
]
