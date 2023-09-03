from django.urls import path, include

from .views import BuyerDashboard, BuyerSettings, BuyerDelete


urlpatterns = [
    path('account/user/', BuyerDashboard.as_view(),
         name='buyer_dashboard'),
    path('account/user/settings/', BuyerSettings.as_view(),
         name='buyer_settings'),
    path('account/user/delete/', BuyerDelete.as_view(), name='buyer_delete'),
]
