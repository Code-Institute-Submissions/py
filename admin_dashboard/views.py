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
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.http import HttpResponse, Http404
import os
from django.http import HttpResponseForbidden
# Local Imports
from homepage.models import UserProfile, STATUS, Comment, Like
from .forms import AdminDownloadCreationForm
from product_service.models import Download, Service, Product
from product_service.validate_file import validate_file_size
from checkout.models import Order
from product_service.utils import check_rate_limit
from .models import OrderDeletionRecord


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

# CREATE Download instance


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

        form_ready = 1
        if not product and not service:
            form_ready = 0
            form.add_error('product',
                           "Select at least one product or service instance.")
        elif product and service:
            form_ready = 0
            form.add_error('product',
                           "Cannot select 2 instances at the same time.")

        # Validating File MB
        file = request.FILES.get('file')
        if file is not None:
            max_upload_size = 500000000
            if file.size > max_upload_size:
                form.add_error('file',
                               "File size must not exceed 500MB.")
        elif file is None:
            form.add_error('file',
                           "File field cannot be empty.")

        if form_ready and file is not None:
            if form.is_valid():
                download_instance = form.save(commit=False)
                download_instance.save()
                form.save_m2m()
                messages.success(
                    request,
                    "Congratulations! The download instance has been created!")
                return redirect('admin_all_downloads')

        return render(
            request, self.template_name,
            {'form': form})


class DownloadWithToken(View):
    """ Download file protection with: user is_authenticated,
    user has placed an order, secret UUID token for file name,
    str token for url name & renaming of the file when downloading with
    Download model file_name.
    All designed to hide the UUID token as the actual file name.
    Remember to include permission on server production."""

    def get(self, request, download_token, *args, **kwargs):
        try:
            # Rate Limit
            rate_limit_response = check_rate_limit(request)
            if rate_limit_response:
                return rate_limit_response

            # Fetch the download instance associated with the token
            download_instance = Download.objects.get(
                download_token=download_token)

            # If yearly availability has been reached
            if not download_instance.is_valid():
                messages.error(request, '''Awaiting for update:
                 please contact the support team.''')
                raise PermissionDenied(
                    "You are not authorized to access this download.")

            # Check if the user is authorized to download
            if not request.user.is_authenticated:
                raise PermissionDenied(
                    "You are not authorized to access this download.")

            # Check if the user has placed an order
            if not Order.objects.filter(buyer_profile=request.user).exists():
                raise PermissionDenied(
                    "You must have placed an order to access this download.")

            # Construct the file path based on the 'file' field
            file_path = download_instance.file.path

            if os.path.exists(file_path):
                # Get file extension
                file_extension = os.path.splitext(
                    download_instance.file.name)[1]

                # File name
                filename = download_instance.file_name

                # Serve the file
                with open(file_path, 'rb') as file:
                    response = HttpResponse(
                        # direct download, do not display in the browser
                        file.read(), content_type='application/octet-stream')
                    response['Content-Disposition'] = f'attachment; filename="{filename}"'

                # Add file extension
                if file_extension:
                    response['Content-Disposition'] += file_extension
                return response
            else:
                raise Http404("Download file not found.")

        except Download.DoesNotExist:
            raise Http404("Download not found.")


# READ Download instances


class DownloadBaseListView(AdminRequiredMixin, ListView):
    """ Base view for listing Download instances. """
    model = Download

    def get_queryset(self):
        """ Return download instances ordered by creation date."""
        return Download.objects.order_by('file_name')


class DownloadList(DownloadBaseListView):
    """ Read all created download instances template """
    template_name = 'admin-dashboard/all_downloads.html'
    context_object_name = 'admin_all_downloads'


# UPDATE Download instance


class BaseUpdateDownloadView(AdminRequiredMixin, View):
    """Base class for download update view."""
    template_name = None

    def get(self, request, item_id, *args, **kwargs):
        context = self.get_context_data(item_id)
        return render(request, self.template_name, context)

    def get_context_data(self, item_id):

        product = Product.objects.filter(status=2).order_by('-created_on')
        service = Service.objects.filter(status=2).order_by('-created_on')

        download_set = Download.objects.order_by('file_name')
        download_instance = get_object_or_404(
            download_set, pk=item_id)

        status = STATUS

        return {
            "download": download_instance,
            "status": status,
            "product": product,
            "service": service,
            "user_authenticated": self.request.user.is_authenticated
        }


class AdminUpdateDownloadView(BaseUpdateDownloadView):
    """View to update download instance"""
    template_name = 'admin-dashboard/update_download.html'

    def post(self, request, item_id, *args, **kwargs):

        download = get_object_or_404(Download, pk=item_id)

        # Validate file title
        file_name = request.POST.get('file_name')
        file_title_exist = Download.objects.filter(
            file_name=file_name).exists()
        if file_title_exist and file_name != download.file_name:
            messages.error(request, 'Title taken, choose another title!')
            return redirect('admin_all_downloads')
        else:
            download.file_name = request.POST.get('file_name')

        product_post = request.POST.get('product')
        service_post = request.POST.get('service')

        # Handle 'None' values for Product
        if product_post == 'None':
            download.product = None
        elif product_post != 'None':
            try:
                product = Product.objects.get(pk=product_post)
                download.product = product
            except Product.DoesNotExist:
                messages.error(request, 'Product does not exist')

        # Handle 'None' values for Service
        if service_post == 'None':
            download.service = None
        elif service_post != 'None':
            try:
                service = Service.objects.get(pk=service_post)
                download.service = service
            except Service.DoesNotExist:
                messages.error(request, 'Service does not exist')

        # Extra validation
        form_ready = 1
        if product_post == 'None' and service_post == 'None':
            form_ready = 0
            messages.error(request,
                           "Select at least one product or service instance.")
        elif product_post != 'None' and service_post != 'None':
            form_ready = 0
            messages.error(request,
                           "Cannot select 2 instances at the same time.")

        status = request.POST.get('status')
        download.status = int(status)

        file = request.FILES.get(
            'file')
        if file and validate_file_size(request, file):
            download.file = file

        if form_ready:
            messages.success(
                request, "Congratulations! The download instance has been updated!")
            download.save()

        return redirect('admin_all_downloads')

# DELETE Download instance


class DownloadDelete(AdminRequiredMixin, DeleteView):
    """View for deleting download instances."""
    model = Download
    template_name = None
    allowed_roles = [1]

    def dispatch(self, request, *args, **kwargs):
        download = self.get_object()
        if download.status == 2:
            messages.error(
                request, "Error: product's status must be suspended or draft.")
            return redirect('admin_all_downloads')

        if self.request.user.role not in self.allowed_roles:
            messages.error(
                request, "Error: User does not have the required role")
            return redirect('admin_all_downloads')

        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        item_id = self.kwargs.get('item_id')
        return get_object_or_404(Download, pk=item_id)

    def get_success_url(self):
        messages.success(self.request, 'Download instance has been deleted!')
        return reverse_lazy('admin_all_downloads')

# Order Deletion


class PendingOrderDeletionView(AdminRequiredMixin, View):
    """View for order deletion."""
    template_name = None

    def get(self, request, *args, **kwargs):
        record = OrderDeletionRecord(initiated_by=request.user)
        record.save()
        messages.success(
            request, "Orders with status 'Pending' deleted successfully")
        return redirect(reverse('all_orders_admin'))

# READ Comments


class CommentBaseListView(AdminRequiredMixin, ListView):
    """ Base view for listing Comment instances. """
    model = Comment

    def get_queryset(self):
        """ Return comment instances ordered by creation date."""
        comments = Comment.objects.order_by('-created_on')
        return comments


class CommentList(CommentBaseListView):
    """ Read all created comment instances template """
    template_name = 'admin-dashboard/all_comments.html'
    context_object_name = 'admin_all_comments'

# UPDATE Comments


class BaseUpdateCommentView(AdminRequiredMixin, View):
    """Base class for comment update view."""
    template_name = None

    def get(self, request, comment_id, *args, **kwargs):
        context = self.get_context_data(comment_id)
        return render(request, self.template_name, context)

    def get_context_data(self, comment_id):

        comment_set = Comment.objects.order_by('-created_on')
        comment_instance = get_object_or_404(
            comment_set, pk=comment_id)

        status = STATUS

        return {
            "comment": comment_instance,
            "status": status,
            "user_authenticated": self.request.user.is_authenticated
        }


class AdminUpdateCommentView(BaseUpdateCommentView):
    """View to update comment instance"""
    template_name = 'admin-dashboard/update_comment.html'

    def post(self, request, comment_id, *args, **kwargs):

        comment = get_object_or_404(Comment, pk=comment_id)

        comment_text = request.POST.get('comment')
        status = request.POST.get('status')

        comment.comment = comment_text[:256]
        comment.status = int(status)

        messages.success(
            request, "Congratulations! The comment instance has been updated!")
        comment.save()

        return redirect('admin_all_comments')

# Delete Comments


class CommentDelete(AdminRequiredMixin, DeleteView):
    """View for deleting comment instances."""
    model = Comment
    template_name = None
    allowed_roles = [1]

    def dispatch(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.status == 2:
            messages.error(
                request, "Error: comment's status must be suspended or draft.")
            return redirect('admin_all_comments')

        if self.request.user.role not in self.allowed_roles:
            messages.error(
                request, "Error: User does not have the required role")
            return redirect('admin_all_comments')

        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        comment_id = self.kwargs.get('comment_id')
        return get_object_or_404(Comment, pk=comment_id)

    def get_success_url(self):
        messages.success(self.request, 'Comment instance has been deleted!')
        return reverse_lazy('admin_all_comments')

# LIKES

# READ Likes


class LikeBaseListView(AdminRequiredMixin, ListView):
    """ Base view for listing Like instances. """
    model = Like

    def get_queryset(self):
        """ Return comment instances ordered by creation date."""
        likes = Like.objects.order_by('-created_on')
        return likes


class LikeList(LikeBaseListView):
    """ Read all created like instances template """
    template_name = 'admin-dashboard/all_likes.html'
    context_object_name = 'admin_all_likes'

# # UPDATE Comments


# class BaseUpdateCommentView(AdminRequiredMixin, View):
#     """Base class for comment update view."""
#     template_name = None

#     def get(self, request, comment_id, *args, **kwargs):
#         context = self.get_context_data(comment_id)
#         return render(request, self.template_name, context)

#     def get_context_data(self, comment_id):

#         comment_set = Comment.objects.order_by('-created_on')
#         comment_instance = get_object_or_404(
#             comment_set, pk=comment_id)

#         status = STATUS

#         return {
#             "comment": comment_instance,
#             "status": status,
#             "user_authenticated": self.request.user.is_authenticated
#         }


# class AdminUpdateCommentView(BaseUpdateCommentView):
#     """View to update comment instance"""
#     template_name = 'admin-dashboard/update_comment.html'

#     def post(self, request, comment_id, *args, **kwargs):

#         comment = get_object_or_404(Comment, pk=comment_id)

#         comment_text = request.POST.get('comment')
#         status = request.POST.get('status')

#         comment.comment = comment_text[:256]
#         comment.status = int(status)

#         messages.success(
#             request, "Congratulations! The comment instance has been updated!")
#         comment.save()

#         return redirect('admin_all_comments')

# # Delete Comments


# class CommentDelete(AdminRequiredMixin, DeleteView):
#     """View for deleting comment instances."""
#     model = Comment
#     template_name = None
#     allowed_roles = [1]

#     def dispatch(self, request, *args, **kwargs):
#         comment = self.get_object()
#         if comment.status == 2:
#             messages.error(
#                 request, "Error: comment's status must be suspended or draft.")
#             return redirect('admin_all_comments')

#         if self.request.user.role not in self.allowed_roles:
#             messages.error(
#                 request, "Error: User does not have the required role")
#             return redirect('admin_all_comments')

#         return super().dispatch(request, *args, **kwargs)

#     def get_object(self, queryset=None):
#         comment_id = self.kwargs.get('comment_id')
#         return get_object_or_404(Comment, pk=comment_id)

#     def get_success_url(self):
#         messages.success(self.request, 'Comment instance has been deleted!')
#         return reverse_lazy('admin_all_comments')
