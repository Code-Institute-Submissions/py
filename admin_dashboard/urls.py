from django.urls import path, include

from .views import AdminDashboard


urlpatterns = [
    path('account/admin/', AdminDashboard.as_view(),
         name='admin_dashboard'),
]
