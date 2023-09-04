# Django Imports
from django.shortcuts import render
from django.views import View, generic

# Local imports
from ..admin_dashboard.views import AdminRequiredMixin
from .forms import AdminProductCreationForm
from .models import Product

# ADMIN CREATE Product & Service

# Product


class AdminProductCreation(AdminRequiredMixin, View):
    """Create product instances for the marketplace """
    template_name = 'admin-dashboard/create.html'

    def get(self, request, *args, **kwargs):
        form = AdminProductCreationForm(initial={'author': request.user})

    def post(self, request, *args, **kwargs):
        form = AdminProductCreationForm(request.POST, request.FILES)

        # Check the image size here
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

            return redirect('account_login')
        else:
            return render(
                request, self.template_name,
                {'form': form})
