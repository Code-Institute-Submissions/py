# Django Imports
from django.shortcuts import render
from django.views import View, generic
from django.shortcuts import get_object_or_404, redirect
# Local imports
from admin_dashboard.views import AdminRequiredMixin
from .forms import AdminProductCreationForm, AdminServiceCreationForm
from .models import Product, Service
from homepage.models import STATUS
from .validate_image import validate_image_size

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
        queryset = Service.objects.order_by('-created_on')
        service = get_object_or_404(queryset, slug=slug)
        status = STATUS
        code = service.code.all()
        offer_service = service.service.all()

        return {
            "service": service,
            "status": status,
            "code": code,
            "offer_service": offer_service,
            "user_authenticated": self.request.user.is_authenticated
        }


class AdminUpdateServiceView(BaseUpdateServiceView):
    """View to update service instance"""
    template_name = 'admin-dashboard/update_service.html'

    def post(self, request, slug, *args, **kwargs):

        service = get_object_or_404(Service, slug=slug)

        service.title = request.POST.get('title')

        status = request.POST.get('status')
        service.status = int(status)

        description = request.POST.get('description')
        service.description = description[:264]

        # service.mission = request.POST.get('mission')
        # service.location = request.POST.get('location')

        image = request.FILES.get(
            'image')
        if image and validate_image_size(request, image):
            service.image = image

        service.save()

        messages.success(
            request, "Congratulations! The service instance has been updated!")
        return redirect('admin_service_update', slug=service.slug)
