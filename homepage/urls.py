# Django Imports
from django.urls import path, include

# Local Imports
from .views import (HomepageProductServiceView,
                    AllProductServiceListView,
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

    # USER ROLE
    path('role_redirect/', role_redirect.UserRoleRedirectView.as_view(),
         name='role_redirect'),
]
