from django.urls import path, include

from .views import (AdminProductCreation)


urlpatterns = [
    path('account/admin/create/', AdminProductCreation.as_view(),
         name='admin_creation'),
]
