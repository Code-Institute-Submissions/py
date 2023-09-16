from django.urls import path, include

from .views import (ProductShoppingCartView,
                    ProductAddToCartView)


urlpatterns = [
    path('bag/', ProductShoppingCartView.as_view(),
         name='bag_page'),
    path('bag/add/<product_id>/', ProductAddToCartView.as_view(),
         name='add_to_cart'),
]
