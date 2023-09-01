from django.urls import path, include

from .views import homepage, CustomLoginView, CustomSignupView
from . import role_redirect


urlpatterns = [
    # AUTHENTICATION
    path('login/', CustomLoginView.as_view(),
         name='account_login'),
    path('signup/', CustomSignupView.as_view(),
         name='account_signup'),
    path('', homepage.as_view(), name='homepage'),

    # ROLE
    path('role_redirect/', role_redirect.RoleRedirectView.as_view(),
         name='role_redirect'),
]
