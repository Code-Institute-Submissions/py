from django.urls import path, include

from .views import homepage, CustomLoginView, CustomSignupView


urlpatterns = [
    # AUTHENTICATION
    path('login/', CustomLoginView.as_view(),
         name='account_login'),
    path('signup/', CustomSignupView.as_view(),
         name='account_signup'),
    path('', homepage.as_view(), name='homepage'),
]
