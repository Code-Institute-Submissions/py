from django.urls import path, include

from .views import homepage, CustomLoginView


urlpatterns = [
    # AUTHENTICATION
    path('login/', CustomLoginView.as_view(),
         name='account_login'),
    path('', homepage.as_view(), name='homepage'),
]
