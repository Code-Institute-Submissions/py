from django.urls import path, include

from .views import (ProductAddToCartView,
                    UpdateProductCartView,
                    DeleteProductCartView)


urlpatterns = [
    path('bag/add/product/<product_id>/', ProductAddToCartView.as_view(),
         name='add_to_cart'),
    path('bag/update/product/<product_id>/', UpdateProductCartView.as_view(),
         name='update_cart'),
    path('bag/delete/product/<product_id>/', DeleteProductCartView.as_view(),
         name='delete_from_cart'),
]
