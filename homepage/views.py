from django.shortcuts import render
from django.views import View, generic
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect

# Authentication app imports
from allauth.account.views import LoginView, SignupView, LogoutView

# Local Imports
from .forms import CustomLoginForm, CustomSignupForm
from product_service.models import Product, Service, Transaction

# LOGIN, SIGUNUP & LOGOUT


class CustomLoginView(LoginView):
    """This view renders our custom login form"""
    form_class = CustomLoginForm
    template_name = 'account/login.html'


class CustomSignupView(SignupView):
    """This view renders our custom signup form"""
    form_class = CustomSignupForm
    template_name = 'account/signup.html'


class CustomLogoutView(LogoutView):
    """This view renders our logout page."""
    template_name = 'account/logout.html'

# Cards Display

# Product & Services


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

        products = list(context['products'][:3])
        services = list(Service.objects.filter(
            status=2).order_by('-created_on')[:3])

        product_single = []
        service_single = []

        combined_list = []

        # 1 product, 1 services, 1 product INTENTION
        if products and services:
            product_single.extend(products[:3])
            service_single.extend(services[:3])

            combined_list.extend(products[:1])
            products = products[2:]

            combined_list.extend(services[:1])
            services = services[3:]

            combined_list.extend(products[:1])
            products = products[1:]

        context['combined_items'] = combined_list
        context['product_single'] = product_single
        context['service_single'] = service_single
        return context

# All Product & Services


class AllProductServiceListView(generic.ListView):
    """Dedicated page for displaying list of ALL products & services."""
    model = Product
    template_name = 'all_product_service/all_product_service.html'
    paginate_by = 6

    def get_queryset(self):
        try:
            products = list(Product.objects.filter(
                status=2).order_by('-created_on'))
            services = list(Service.objects.filter(
                status=2).order_by('-created_on'))

            combined_list = self.combine_products_and_services(
                products, services)
            return combined_list
        except Exception as e:
            print(e)
            return []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        combined_list = self.get_queryset()

        paginator = Paginator(combined_list, self.paginate_by)
        page_number = self.request.GET.get('page', 1)

        try:
            page_obj = paginator.page(page_number)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        except PageNotAnInteger:
            page_obj = paginator.page(1)

        context['page_obj'] = page_obj
        context['is_paginated'] = len(combined_list) > self.paginate_by
        return context

    def combine_products_and_services(self, products, services):
        combined_list = []
        while products or services:
            if products:
                combined_list.append(products.pop(0))
            if services:
                combined_list.append(services.pop(0))
            if products:
                combined_list.append(products.pop(0))
        return combined_list

# All Product


class AllProductListView(generic.ListView):
    """Dedicated page for displaying list of all product instances."""
    model = Product
    template_name = 'all_product_service/all_product.html'
    paginate_by = 6
    context_object_name = 'product_all'

    def get_queryset(self):
        try:
            products = list(Product.objects.filter(
                status=2).order_by('-created_on'))
            return products
        except Exception as e:
            print(e)
            return []

# All Services


class AllServiceListView(generic.ListView):
    """Dedicated page for displaying list of all service instances."""
    model = Service
    template_name = 'all_product_service/all_service.html'
    paginate_by = 6
    context_object_name = 'service_all'

    def get_queryset(self):
        try:
            services = list(Service.objects.filter(
                status=2).order_by('-created_on'))
            return services
        except Exception as e:
            print(e)
            return []

# Single Product


class SingleProductView(View):
    """View for listing SINGLE product instances."""

    def get(self, request, slug, *args, **kwargs):
        queryset = Product.objects.order_by('-created_on')
        product = get_object_or_404(queryset, slug=slug)

        # Check if user voted or not
        if request.user.is_authenticated:
            has_purchased = Transaction.objects.filter(
                buyer=request.user, product=product).exists()
        else:
            has_purchased = False

        return render(request, "single_product_service/single_product.html",
                      {
                          "product": product,
                          "has_purchased": has_purchased,
                          "user_authenticated": request.user.is_authenticated
                      })
