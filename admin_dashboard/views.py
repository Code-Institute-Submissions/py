# Django Imports
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views import generic
from django.shortcuts import get_object_or_404, redirect
from django import forms
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import logout
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy, reverse
from django.contrib import messages

# Local Imports
from homepage.models import UserProfile


class AdminRequiredMixin(UserPassesTestMixin):
    """Mixin to check for admin role (role 1) for access control."""

    def test_func(self):
        user_profile = self.request.user
        return user_profile and user_profile.role == 1


class AdminDashboard(AdminRequiredMixin, generic.DetailView):
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
