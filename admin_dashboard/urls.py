from django.urls import path, include

from .views import (AdminDashboard, AdminSettingsView,
                    AdminPasswordChange, AdminRole, AdminDownloadCreation,
                    DownloadList)


urlpatterns = [
    # Admin Settings
    path('account/admin/', AdminDashboard.as_view(),
         name='admin_dashboard'),
    path('account/admin/settings/', AdminSettingsView.as_view(),
         name='admin_settings'),
    path('account/admin/password/', AdminPasswordChange.as_view(),
         name='admin_change_password'),
    path('account/admin/role/', AdminRole.as_view(),
         name='admin_role'),
    path('account/admin/download/create/', AdminDownloadCreation.as_view(),
         name='admin_download_create'),
    path('account/admin/download/all/', DownloadList.as_view(),
         name='admin_all_downloads'),
]
