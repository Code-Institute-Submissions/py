# Django Imports
from django.urls import path, include

# Local Imports
from .views import (HomepageProductServiceView,
                    AllProductServiceListView,
                    AllProductListView,
                    AllServiceListView,
                    SingleProductView,
                    SingleServiceView,
                    SortedProductServiceListView,
                    CustomLoginView,
                    CustomSignupView,
                    CustomLogoutView,
                    ProductLikePost,
                    ServiceLikePost,
                    NewsletterPost,
                    ContactView,
                    FAQView,
                    TermsView,
                    PrivacyView,)
from . import role_redirect


urlpatterns = [

    # USER AUTHENTICATION
    path('login/', CustomLoginView.as_view(),
         name='account_login'),
    path('signup/', CustomSignupView.as_view(),
         name='account_signup'),
    path('logout/', CustomLogoutView.as_view(),
         name='account_logout'),

    # HOMEPAGE
    path('', HomepageProductServiceView.as_view(),
         name='product_service_instance'),
    path('all/', AllProductServiceListView.as_view(),
         name='combined_items_all'),
    path('all/product/', AllProductListView.as_view(),
         name='product_all'),
    path('all/service/', AllServiceListView.as_view(),
         name='service_all'),
    path('product/<slug:slug>', SingleProductView.as_view(),
         name='single_product'),
    path('service/<slug:slug>', SingleServiceView.as_view(),
         name='single_service'),
    path('sort/', SortedProductServiceListView.as_view(),
         name='sorted'),

    # Product Like
    path('product/like/<slug:slug>', ProductLikePost.as_view(),
         name='product_like'),

    # Service Like
    path('service/like/<slug:slug>', ServiceLikePost.as_view(),
         name='service_like'),

    # Newsletter
    path('newsletter/add/', NewsletterPost.as_view(),
         name='newsletter'),

    # USER ROLE
    path('role_redirect/', role_redirect.UserRoleRedirectView.as_view(),
         name='role_redirect'),

    # Contact Page & FAQ
    path('contact/', ContactView.as_view(),
         name='contact_form'),
    path('faq/', FAQView.as_view(),
         name='faq_page'),

    # Terms & Policy
    path('terms/', TermsView.as_view(),
         name='terms_page'),
    path('policy/', PrivacyView.as_view(),
         name='policy_page'),
]
