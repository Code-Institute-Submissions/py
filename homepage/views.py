from django.shortcuts import render
from django.views import View, generic
from django.utils import timezone

# Authentication app imports
from allauth.account.views import LoginView, SignupView, LogoutView

# Local Imports
from .forms import CustomLoginForm, CustomSignupForm
from product_service.models import Product, Service

# LOGIN, SIGUNUP & LOGOUT


class CustomLoginView(LoginView):
    """This view renders our custom login form"""
    form_class = CustomLoginForm
    template_name = 'account/login.html'

#     def get_success_url(self):
#         user_id = self.request.user.id
#         return reverse_lazy('user_dashboard', kwargs={'pk': user_id})


class CustomSignupView(SignupView):
    """This view renders our custom signup form"""
    form_class = CustomSignupForm
    template_name = 'account/signup.html'


class CustomLogoutView(LogoutView):
    """This view renders our logout page."""
    template_name = 'account/logout.html'


# class homepage(generic.TemplateView):
#     template_name = 'home/homepage.html'

# Cards Display

# Product


class ProductBaseListView(generic.ListView):
    """Base view for listing products based on these conditions."""
    model = Product

    def get_queryset(self):
        """Return products with a status of 2, ordered by creation date."""
        products = Product.objects.filter(status=2).order_by('-created_on')[:3]

        return products


class HomepageProductServiceView(ProductBaseListView):
    """Frontend main page displaying the list of products & services."""
    template_name = 'home/homepage.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        products = list(context['products'][:2])
        services = list(Service.objects.filter(
            status=2).order_by('-created_on')[:1])

        combined_list = []

        # 1 product, 1 services, 1 product INTENTION
        if products and services:
            combined_list.extend(products[:1])
            products = products[1:]
            combined_list.extend(services[:1])
            services = services[1:]
            combined_list.extend(products[:1])
            products = products[1:]

        context['combined_items'] = combined_list
        return context
