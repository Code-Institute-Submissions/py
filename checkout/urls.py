# Django Imports
from django.urls import path, include

# Local Imports
from .views import (Checkout)
from .stripe import (StripeCheckoutView, StripeCheckoutSuccess)
from .webhooks import StripeWebhookView

urlpatterns = [

    path('checkout/', Checkout.as_view(),
         name='checkout_page'),
    path('checkout/stripe/form/', StripeCheckoutView.as_view(),
         name='checkout_stripe_form'),
    path('checkout/success/<order_number>', StripeCheckoutSuccess.as_view(),
         name='checkout_success'),
    # For Stripe to post events (Webhook)
    path('webhook/', StripeWebhookView.as_view(),
         name='webhook'),
]
