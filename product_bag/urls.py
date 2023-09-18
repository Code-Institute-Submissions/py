from django.urls import path, include

from .views import (ProductShoppingCartView,
                    ProductAddToCartView,
                    UpdateProductCartView)


urlpatterns = [
    path('bag/', ProductShoppingCartView.as_view(),
         name='bag_page'),
    path('bag/add/<product_id>/', ProductAddToCartView.as_view(),
         name='add_to_cart'),
    path('bag/update/<product_id>/', UpdateProductCartView.as_view(),
         name='update_cart'),
]
