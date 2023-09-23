# Django Imports
from django.urls import path, include

# Local Imports
from .views import (Checkout)
from .stripe import StripeCheckoutSessionView

urlpatterns = [

    path('checkout/', Checkout.as_view(),
         name='checkout_page'),
    path('checkout/stripe/', StripeCheckoutSessionView.as_view(),
         name='stripe_checkout'),
]
