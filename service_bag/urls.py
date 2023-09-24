from django.urls import path, include

from .views import (ServiceAddToCartView,
                    UpdateServiceCartView,
                    DeleteServiceCartView)


urlpatterns = [
    path('bag/add/service/<service_id>/', ServiceAddToCartView.as_view(),
         name='add_to_cart_service'),
    path('bag/update/service/<service_id>/', UpdateServiceCartView.as_view(),
         name='update_cart_service'),
    path('bag/delete/service/<service_id>/', DeleteServiceCartView.as_view(),
         name='delete_from_cart_service'),
]
