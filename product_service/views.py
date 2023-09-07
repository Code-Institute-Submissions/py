# Django Imports
from django.shortcuts import render
from django.views import View, generic
from django.shortcuts import get_object_or_404, redirect
# Local imports
from admin_dashboard.views import AdminRequiredMixin
from .forms import AdminProductCreationForm, AdminServiceCreationForm
from .models import Product, Service

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
        uploaded_image = request.FILES.get('image')
        if uploaded_image:
            max_upload_size = 500000
            if uploaded_image.size > max_upload_size:
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

        # Validating Image in KB
        uploaded_image = request.FILES.get('image')
        if uploaded_image:
            max_upload_size = 500000
            if uploaded_image.size > max_upload_size:
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
        """ Return Product instances ordered by creation date."""
        return Service.objects.order_by('-created_on')


class ServiceList(ServiceBaseListView):
    """ Read all created Vote Cards on Admin's Dashboard"""
    template_name = 'admin-dashboard/all_services.html'
    context_object_name = 'admin_all_services'
