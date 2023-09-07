# Django Imports
from django.shortcuts import render
from django.views import View, generic
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

# Local imports
from admin_dashboard.views import AdminRequiredMixin
from .forms import AdminProductCreationForm, AdminServiceCreationForm
from .models import Product, Service, Category, ServiceType, CodeType
from homepage.models import STATUS
from .validate_image import validate_image_size
from .models import SCOPE_TYPE

# ADMIN CREATE Product & Service

# Product Creation


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

            return redirect('admin_product_creation')
        else:
            return render(
                request, self.template_name,
                {'form': form})

# Service Creation


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

            return redirect('admin_service_creation')
        else:
            return render(
                request, self.template_name,
                {'form': form})

# Service Management List


class ServiceBaseListView(AdminRequiredMixin, generic.ListView):
    """ Base view for listing Service instances."""
    model = Service

    def get_queryset(self):
        """ Return service instances ordered by creation date."""
        return Service.objects.order_by('-created_on')


class ServiceList(ServiceBaseListView):
    """ Read all created service instances ftempalte"""
    template_name = 'admin-dashboard/all_services.html'
    context_object_name = 'admin_all_services'

# UPDATE Service Instance


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
