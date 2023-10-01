# Django Imports
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import ListView, DetailView, View
from django.shortcuts import render, get_object_or_404, redirect
from django import forms
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import logout
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy, reverse
from django.contrib import messages

# Local Imports
from homepage.models import UserProfile
from .forms import AdminDownloadCreationForm


class AdminRequiredMixin(UserPassesTestMixin):
    """Mixin to check for admin role (role 1) for access control."""

    def test_func(self):
        user_profile = self.request.user
        return user_profile and user_profile.role == 1


class AdminDashboard(AdminRequiredMixin, DetailView):
    """Display the dashboard for users with 'role 1'. Redirect to the same page."""
    model = UserProfile
    template_name = 'admin-dashboard/dashboard.html'
    context_object_name = 'admin_dashboard'

    def get_object(self, queryset=None):
        return get_object_or_404(UserProfile, pk=self.request.user.pk)

    def get_success_url(self):
        messages.success(
            self.request, 'You have been logged in successfully!')
        return self.request.path

# Settings


class AdminSettingsForm(forms.ModelForm):
    """Set necessary form fields for settings"""
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'email', 'username']

# UPDATE settings


class AdminSettingsView(AdminRequiredMixin, UpdateView):
    """Handle Admin Data Update in settings. Redirect to the same page."""
    model = UserProfile
    form_class = AdminSettingsForm
    template_name = 'admin-dashboard/settings.html'
    context_object_name = 'admin_settings'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        messages.success(
            self.request, 'Your account has been updated!')
        return self.request.path

    def form_valid(self, form):
        username = self.request.POST.get('username')
        if UserProfile.objects.filter(username=username).exclude(pk=self.request.user.pk).exists():
            messages.error(self.request, 'Username already exists.')
            return self.form_invalid(form)
        else:
            return super().form_valid(form)

# PASSWORD Change


class AdminPasswordChangeForm(PasswordChangeForm):
    """Form for changing the admin's password."""

    class Meta:
        fields = ['old_password', 'new_password1', 'new_password2']


class AdminPasswordChange(AdminRequiredMixin, PasswordChangeView):
    """View for changing the admin's password. Redirect to the same page."""
    template_name = 'admin-dashboard/password_change.html'
    form_class = AdminPasswordChangeForm
    context_object_name = 'admin_change_password'

    def get_success_url(self):
        messages.success(self.request, 'Your password has changed!')
        return self.request.path


class AdminRole(AdminDashboard):
    """Redender view for role info display"""
    template_name = 'admin-dashboard/role.html'

# Download  Functionality

# Download Creation instance


class AdminDownloadCreation(AdminRequiredMixin, View):
    """Create Download instances for the product & service """
    template_name = 'admin-dashboard/create_download.html'

    def get(self, request, *args, **kwargs):
        form = AdminDownloadCreationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = AdminDownloadCreationForm(request.POST, request.FILES)

        product = request.POST.get('product')
        service = request.POST.get('service')

        single_instance = 1
        if not product and not service:
            form.add_error('product',
                           "Select at least one product or service instance.")
        elif product and service:
            single_instance = 0
            form.add_error('product',
                           "Cannot select 2 instances at the same time.")

        # Validating File MB
        file = request.FILES.get('file')
        print(f'FILE CONDITION: {file}')
        if file is not None:
            max_upload_size = 500000000
            if file.size > max_upload_size:
                form.add_error('file',
                               "File size must not exceed 500MB.")
        elif file is None:
            form.add_error('file',
                           "File field cannot be empty.")

        if single_instance and file is not None:
            if form.is_valid():
                download_instance = form.save(commit=False)
                download_instance.save()
                form.save_m2m()
                messages.success(
                    request,
                    "Congratulations! The download instance has been created!")
                return redirect('admin_role')

        return render(
            request, self.template_name,
            {'form': form})

# # READ Product instances


# class ProductBaseListView(AdminRequiredMixin, ListView):
#     """ Base view for listing Product instances."""
#     model = Product

#     def get_queryset(self):
#         """ Return product instances ordered by creation date."""
#         return Product.objects.order_by('-created_on')


# class ProductList(ProductBaseListView):
#     """ Read all created product instances tempalte"""
#     template_name = 'admin-dashboard/all_products.html'
#     context_object_name = 'admin_all_products'


# # UPDATE Product instance


# class BaseUpdateProductView(AdminRequiredMixin, View):
#     """Base class for product list view."""
#     template_name = None

#     def get(self, request, slug, *args, **kwargs):
#         context = self.get_context_data(slug)
#         return render(request, self.template_name, context)

#     def get_context_data(self, slug):
#         categories = Category.objects.all()
#         services = ServiceType.objects.all()
#         codes = CodeType.objects.all()

#         queryset = Product.objects.order_by('-created_on')
#         product = get_object_or_404(queryset, slug=slug)

#         # Dynamically filter choices for
#         # download_url based on the current instance
#         related_downloads = Download.objects.filter(product=product)

#         status = STATUS
#         scope = SCOPE_TYPE
#         offer_code = product.code.all()
#         offer_service = product.service.all()
#         files_selected = product.download_url.all()

#         return {
#             "categories": categories,
#             "services": services,
#             "codes": codes,

#             "product": product,
#             "status": status,
#             "scope": scope,
#             "offer_code": offer_code,
#             "offer_service": offer_service,
#             "related_downloads": related_downloads,
#             "files_selected": files_selected,
#             "user_authenticated": self.request.user.is_authenticated
#         }


# class AdminUpdateProductView(BaseUpdateProductView):
#     """View to update product instance"""
#     template_name = 'admin-dashboard/update_product.html'

#     def post(self, request, slug, *args, **kwargs):

#         product = get_object_or_404(Product, slug=slug)

#         product.title = request.POST.get('title')
#         product.sku = request.POST.get('sku')
#         product.price = request.POST.get('price')

#         product.category = Category.objects.get(
#             pk=request.POST.get('category'))

#         status = request.POST.get('status')
#         product.status = int(status)

#         type = request.POST.get('type')
#         product.type = int(type)

#         code = request.POST.getlist('code')
#         product.code.set(code)

#         services = request.POST.getlist('service')
#         product.service.set(services)

#         product.preview = request.POST.get('preview')

#         product.docs = request.POST.get('docs')

#         description = request.POST.get('description')
#         product.description = description[:528]

#         product.excerpt = request.POST.get('excerpt')

#         image = request.FILES.get(
#             'image')
#         if image and validate_image_size(request, image):
#             product.image = image

#         product.image_url = request.POST.get('image_url')

#         related_downloads = request.POST.getlist('related_downloads')
#         product.download_url.set(related_downloads)

#         product.save()

#         messages.success(
#             request, "Congratulations! The product instance has been updated!")
#         return redirect('admin_product_update', slug=product.slug)

# # DELETE Product instance


# class ProductDelete(AdminRequiredMixin, DeleteView):
#     """View for deleting product instances."""
#     model = Product
#     template_name = None
#     allowed_roles = [1]

#     def dispatch(self, request, *args, **kwargs):
#         product = self.get_object()
#         if product.status == 2:
#             messages.error(
#                 request, "Error: product's status must be suspended or draft.")
#             return redirect('admin_all_products')

#         if self.request.user.role not in self.allowed_roles:
#             messages.error(
#                 request, "Error: User does not have the required role")
#             return redirect('admin_all_products')

#         return super().dispatch(request, *args, **kwargs)

#     def get_object(self, queryset=None):
#         slug = self.kwargs.get('slug')
#         return get_object_or_404(Product, slug=slug)

#     def get_success_url(self):
#         messages.success(self.request, 'Product Instance has been deleted!')
#         return reverse_lazy('admin_all_products')
