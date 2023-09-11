# Django Imports
from django.shortcuts import render
from django.views import View, generic
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.views.generic.edit import DeleteView
from django.core.exceptions import PermissionDenied
from django.urls import reverse, reverse_lazy

# Local imports
from admin_dashboard.views import AdminRequiredMixin
from .forms import AdminProductCreationForm, AdminServiceCreationForm
from .models import Product, Service, Category, ServiceType, CodeType
from homepage.models import STATUS
from .validate_image import validate_image_size
from .models import SCOPE_TYPE

# ADMIN CREATE Product & Service

# Product Creation instance


class AdminProductCreation(AdminRequiredMixin, View):
    """Create product instances for the marketplace """
    template_name = 'admin-dashboard/create_product.html'

    def get(self, request, *args, **kwargs):
        form = AdminProductCreationForm(initial={'author': request.user})
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = AdminProductCreationForm(request.POST, request.FILES)

        # Validating Image KB
        image = request.FILES.get('image')
        if image:
            max_upload_size = 500000
            if image.size > max_upload_size:
                form.add_error('image',
                               "File size must not exceed 500KB.")

        if form.is_valid():
            product_instance = form.save(commit=False)
            product_instance.author = request.user
            product_instance.save()
            form.save_m2m()
            messages.success(
                request,
                "Congratulations! The product instance has been created!")
            return redirect('admin_all_products')
        else:
            return render(
                request, self.template_name,
                {'form': form})

# READ Product instances


class ProductBaseListView(AdminRequiredMixin, generic.ListView):
    """ Base view for listing Product instances."""
    model = Product

    def get_queryset(self):
        """ Return product instances ordered by creation date."""
        return Product.objects.order_by('-created_on')


class ProductList(ProductBaseListView):
    """ Read all created product instances tempalte"""
    template_name = 'admin-dashboard/all_products.html'
    context_object_name = 'admin_all_products'


# UPDATE Product instance


class BaseUpdateProductView(AdminRequiredMixin, View):
    """Base class for product list view."""
    template_name = None

    def get(self, request, slug, *args, **kwargs):
        context = self.get_context_data(slug)
        return render(request, self.template_name, context)

    def get_context_data(self, slug):
        categories = Category.objects.all()
        services = ServiceType.objects.all()
        codes = CodeType.objects.all()

        queryset = Product.objects.order_by('-created_on')
        product = get_object_or_404(queryset, slug=slug)
        status = STATUS
        scope = SCOPE_TYPE
        offer_code = product.code.all()
        offer_service = product.service.all()

        return {
            "categories": categories,
            "services": services,
            "codes": codes,

            "product": product,
            "status": status,
            "scope": scope,
            "offer_code": offer_code,
            "offer_service": offer_service,
            "user_authenticated": self.request.user.is_authenticated
        }


class AdminUpdateProductView(BaseUpdateProductView):
    """View to update product instance"""
    template_name = 'admin-dashboard/update_product.html'

    def post(self, request, slug, *args, **kwargs):

        product = get_object_or_404(Product, slug=slug)

        product.title = request.POST.get('title')
        product.sku = request.POST.get('sku')
        product.price = request.POST.get('price')

        product.category = Category.objects.get(
            pk=request.POST.get('category'))

        status = request.POST.get('status')
        product.status = int(status)

        type = request.POST.get('type')
        product.type = int(type)

        code = request.POST.getlist('code')
        product.code.set(code)

        services = request.POST.getlist('service')
        product.service.set(services)

        product.preview = request.POST.get('preview')

        product.docs = request.POST.get('docs')

        description = request.POST.get('description')
        product.description = description[:264]

        product.excerpt = request.POST.get('excerpt')

        image = request.FILES.get(
            'image')
        if image and validate_image_size(request, image):
            product.image = image

        product.image_url = request.POST.get('image_url')

        product.save()

        messages.success(
            request, "Congratulations! The product instance has been updated!")
        return redirect('admin_product_update', slug=product.slug)

# DELETE Product instance


class ProductDelete(AdminRequiredMixin, DeleteView):
    """View for deleting product instances."""
    model = Product
    template_name = None
    allowed_roles = [1]

    def dispatch(self, request, *args, **kwargs):
        product = self.get_object()
        if product.status == 2:
            messages.error(
                request, "Error: product's status must be suspended or draft.")
            return redirect('admin_all_products')

        if self.request.user.role not in self.allowed_roles:
            messages.error(
                request, "Error: User does not have the required role")
            return redirect('admin_all_products')

        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Product, slug=slug)

    def get_success_url(self):
        messages.success(self.request, 'Product Instance has been deleted!')
        return reverse_lazy('admin_all_products')


# CREATE Service instance


class AdminServiceCreation(AdminRequiredMixin, View):
    """Create service instances for the marketplace """
    template_name = 'admin-dashboard/create_service.html'

    def get(self, request, *args, **kwargs):
        form = AdminServiceCreationForm(initial={'author': request.user})
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = AdminServiceCreationForm(request.POST, request.FILES)

        # Validating Image KB
        image = request.FILES.get('image')
        if image:
            max_upload_size = 500000
            if image.size > max_upload_size:
                form.add_error('image',
                               "File size must not exceed 500KB.")

        if form.is_valid():
            service_instance = form.save(commit=False)
            service_instance.author = request.user
            service_instance.save()
            form.save_m2m()
            messages.success(
                request,
                "Congratulations! The service instance has been created!")
            return redirect('admin_all_services')
        else:
            return render(
                request, self.template_name,
                {'form': form})

# READ Service instances


class ServiceBaseListView(AdminRequiredMixin, generic.ListView):
    """ Base view for listing Service instances."""
    model = Service

    def get_queryset(self):
        """ Return service instances ordered by creation date."""
        return Service.objects.order_by('-created_on')


class ServiceList(ServiceBaseListView):
    """ Read all created service instances tempalte"""
    template_name = 'admin-dashboard/all_services.html'
    context_object_name = 'admin_all_services'

# UPDATE Service instance


class BaseUpdateServiceView(AdminRequiredMixin, View):
    """Base class for service list view."""
    template_name = None

    def get(self, request, slug, *args, **kwargs):
        context = self.get_context_data(slug)
        return render(request, self.template_name, context)

    def get_context_data(self, slug):
        categories = Category.objects.all()
        services = ServiceType.objects.all()
        codes = CodeType.objects.all()

        queryset = Service.objects.order_by('-created_on')
        service = get_object_or_404(queryset, slug=slug)
        status = STATUS
        scope = SCOPE_TYPE
        offer_code = service.code.all()
        offer_service = service.service.all()

        return {
            "categories": categories,
            "services": services,
            "codes": codes,

            "service": service,
            "status": status,
            "scope": scope,
            "offer_code": offer_code,
            "offer_service": offer_service,
            "user_authenticated": self.request.user.is_authenticated
        }


class AdminUpdateServiceView(BaseUpdateServiceView):
    """View to update service instance"""
    template_name = 'admin-dashboard/update_service.html'

    def post(self, request, slug, *args, **kwargs):

        service = get_object_or_404(Service, slug=slug)

        service.title = request.POST.get('title')
        service.sku = request.POST.get('sku')
        service.price = request.POST.get('price')

        service.category = Category.objects.get(
            pk=request.POST.get('category'))

        status = request.POST.get('status')
        service.status = int(status)

        type = request.POST.get('type')
        service.type = int(type)

        code = request.POST.getlist('code')
        service.code.set(code)

        services = request.POST.getlist('service')
        service.service.set(services)

        service.preview = request.POST.get('preview')

        service.docs = request.POST.get('docs')

        description = request.POST.get('description')
        service.description = description[:264]

        service.excerpt = request.POST.get('excerpt')

        image = request.FILES.get(
            'image')
        if image and validate_image_size(request, image):
            service.image = image

        service.image_url = request.POST.get('image_url')

        service.save()

        messages.success(
            request, "Congratulations! The service instance has been updated!")
        return redirect('admin_service_update', slug=service.slug)

# DELETE Service instance


class ServiceDelete(AdminRequiredMixin, DeleteView):
    """View for deleting service instances."""
    model = Service
    template_name = None
    allowed_roles = [1]

    def dispatch(self, request, *args, **kwargs):
        service = self.get_object()
        if service.status == 2:
            messages.error(
                request, "Error: service's status must be suspended or draft.")
            return redirect('admin_all_services')

        if self.request.user.role not in self.allowed_roles:
            messages.error(
                request, "Error: User does not have the required role")
            return redirect('admin_all_services')

        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Service, slug=slug)

    def get_success_url(self):
        messages.success(self.request, 'Service Instance has been deleted!')
        return reverse_lazy('admin_all_services')
