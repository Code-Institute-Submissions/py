from django.urls import path, include

from .views import UserDashboard


urlpatterns = [
    path('account/user/', UserDashboard.as_view(),
         name='user_dashboard'),
]
