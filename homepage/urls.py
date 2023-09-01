# Django Imports
from django.urls import path, include

# Local Imports
from .views import homepage, CustomLoginView, CustomSignupView
from . import role_redirect


urlpatterns = [
    # USER AUTHENTICATION
    path('login/', CustomLoginView.as_view(),
         name='account_login'),
    path('signup/', CustomSignupView.as_view(),
         name='account_signup'),
    path('', homepage.as_view(), name='homepage'),

    # USER ROLE
    path('role_redirect/', role_redirect.UserRoleRedirectView.as_view(),
         name='role_redirect'),
]
