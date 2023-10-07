from django.urls import path, include

from .views import (AdminDashboard, AdminSettingsView,
                    AdminPasswordChange, AdminRole, AdminDownloadCreation,
                    DownloadWithToken,
                    DownloadList, AdminUpdateDownloadView, DownloadDelete,
                    PendingOrderDeletionView)


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
    path('account/admin/download/file/<int:item_id>/', AdminUpdateDownloadView.as_view(),
         name='admin_update_download'),
    path('account/admin/download/file/delete/<int:item_id>/',
         DownloadDelete.as_view(), name='admin_delete_download'),
    path('media/downloads/<str:download_token>/', DownloadWithToken.as_view(),
         name='download_with_token'),
    path('account/admin/orders/delete/', PendingOrderDeletionView.as_view(),
         name='orders_delete'),

]
