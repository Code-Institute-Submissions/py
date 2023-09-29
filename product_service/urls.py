from django.urls import path, include

from .views import (AdminProductCreation,
                    ProductList,
                    AdminUpdateProductView,
                    ProductDelete,

                    AdminServiceCreation,
                    ServiceList,
                    AdminUpdateServiceView,
                    ServiceDelete,
                    ShoppingCartView,
                    AdminOrderListView,
                    BuyerOrderListView,)


urlpatterns = [
    # Admin product features
    path('account/admin/create/product/', AdminProductCreation.as_view(),
         name='admin_product_creation'),
    path('account/admin/all_product/', ProductList.as_view(),
         name='admin_all_products'),
    path('account/admin/product/<slug:slug>/',
         AdminUpdateProductView.as_view(),
         name='admin_product_update'),
    path('account/admin/product/delete/<slug:slug>/',
         ProductDelete.as_view(), name='delete_product'),

    # Admin service features
    path('account/admin/create/service/', AdminServiceCreation.as_view(),
         name='admin_service_creation'),
    path('account/admin/all_service/', ServiceList.as_view(),
         name='admin_all_services'),
    path('account/admin/service/<slug:slug>/',
         AdminUpdateServiceView.as_view(),
         name='admin_service_update'),
    path('account/admin/service/delete/<slug:slug>/',
         ServiceDelete.as_view(), name='delete_service'),

    # Admin & Buyer Order Management
    path('account/admin/order/', AdminOrderListView.as_view(),
         name='all_orders_admin'),
    path('account/user/order/', BuyerOrderListView.as_view(),
         name='all_orders_user'),

    # Frontend Bag View
    path('bag/', ShoppingCartView.as_view(),
         name='bag_page'),
]
