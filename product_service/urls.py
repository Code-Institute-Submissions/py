from django.urls import path, include

from .views import (AdminProductCreation,
                    AdminServiceCreation,
                    ServiceList,
                    AdminUpdateServiceView)


urlpatterns = [
    path('account/admin/create/product/', AdminProductCreation.as_view(),
         name='admin_product_creation'),
    path('account/admin/create/service/', AdminServiceCreation.as_view(),
         name='admin_service_creation'),
    path('account/admin/all_service/', ServiceList.as_view(),
         name='admin_all_services'),
    path('account/admin/service/<slug:slug>/', AdminUpdateServiceView.as_view(),
         name='admin_service_update'),
]
