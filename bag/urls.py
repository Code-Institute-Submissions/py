from django.urls import path, include

from .views import (ShoppingBagView)


urlpatterns = [
    path('bag/', ShoppingBagView.as_view(),
         name='bag_page'),
]
