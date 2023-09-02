from django.urls import path, include

from .views import AdminDashboard, AdminSettingsView


urlpatterns = [
    path('account/admin/', AdminDashboard.as_view(),
         name='admin_dashboard'),
    path('account/admin/settings/', AdminSettingsView.as_view(),
         name='admin_settings'),
]
