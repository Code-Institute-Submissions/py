# Django Imports
from django.urls import path, include

# Local Imports
from .views import (HomepageProductServiceView,
                    AllProductServiceListView,
                    AllProductListView,
                    AllServiceListView,
                    SingleProductView,
                    SingleServiceView,
                    SortedProductServiceListView,
                    CustomLoginView,
                    CustomSignupView,
                    CustomLogoutView)
from . import role_redirect


urlpatterns = [

    # USER AUTHENTICATION
    path('login/', CustomLoginView.as_view(),
         name='account_login'),
    path('signup/', CustomSignupView.as_view(),
         name='account_signup'),
    path('logout/', CustomLogoutView.as_view(),
         name='account_logout'),

    # HOMEPAGE
    path('', HomepageProductServiceView.as_view(),
         name='product_service_instance'),
    path('all/', AllProductServiceListView.as_view(),
         name='combined_items_all'),
    path('all/product/', AllProductListView.as_view(),
         name='product_all'),
    path('all/service/', AllServiceListView.as_view(),
         name='service_all'),
    path('product/<slug:slug>', SingleProductView.as_view(),
         name='single_product'),
    path('service/<slug:slug>', SingleServiceView.as_view(),
         name='single_service'),
    path('sort/', SortedProductServiceListView.as_view(),
         name='sorted'),


    # USER ROLE
    path('role_redirect/', role_redirect.UserRoleRedirectView.as_view(),
         name='role_redirect'),
]
