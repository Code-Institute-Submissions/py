from django.urls import path, include

from .views import BuyerDashboard, BuyerSettings


urlpatterns = [
    path('account/user/', BuyerDashboard.as_view(),
         name='buyer_dashboard'),
    path('account/user/settings/', BuyerSettings.as_view(),
         name='buyer_settings'),
]
