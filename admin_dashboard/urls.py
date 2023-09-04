from django.urls import path, include

from .views import (AdminDashboard, AdminSettingsView,
                    AdminPasswordChange, AdminRole)
from ..product_service.views import AdminProductCreation


urlpatterns = [
    path('account/admin/', AdminDashboard.as_view(),
         name='admin_dashboard'),
    path('account/admin/settings/', AdminSettingsView.as_view(),
         name='admin_settings'),
    path('account/admin/password/', AdminPasswordChange.as_view(),
         name='admin_change_password'),
    path('account/admin/role/', AdminRole.as_view(),
         name='admin_role'),
    path('account/admin/create/', AdminProductCreation.as_view(),
         name='admin_creation'),
]
