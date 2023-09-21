# Django Imports
from django.urls import path, include

# Local Imports
from .views import (Checkout)


urlpatterns = [

    path('checkout/', Checkout.as_view(),
         name='checkout_page'),
]
