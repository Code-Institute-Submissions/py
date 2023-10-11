from django.urls import path, include

from .views import (AdminDashboard, AdminSettingsView,
                    AdminPasswordChange, AdminRole, AdminDownloadCreation,
                    DownloadWithToken,
                    DownloadList, AdminUpdateDownloadView, DownloadDelete,
                    PendingOrderDeletionView, CommentList,)


urlpatterns = [
    # Dashboard
    path('account/admin/', AdminDashboard.as_view(),
         name='admin_dashboard'),

    # Settings
    path('account/admin/settings/', AdminSettingsView.as_view(),
         name='admin_settings'),
    path('account/admin/password/', AdminPasswordChange.as_view(),
         name='admin_change_password'),
    path('account/admin/role/', AdminRole.as_view(),
         name='admin_role'),

    # Download
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

    # Orders Delete
    path('account/admin/orders/delete/', PendingOrderDeletionView.as_view(),
         name='orders_delete'),

    # Comments
    path('account/admin/comments/', CommentList.as_view(),
         name='admin_all_comments'),
]
