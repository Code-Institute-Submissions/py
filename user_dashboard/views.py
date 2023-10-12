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
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Local Imports
from homepage.models import UserProfile

# User Dashboard


@method_decorator(login_required, name='dispatch')
class BuyerRequiredMixin(UserPassesTestMixin):
    """Mixin to check for user role (role 0) for access control."""

    def test_func(self):
        user_profile = self.request.user
        return user_profile and user_profile.role == 0


@method_decorator(login_required, name='dispatch')
class BuyerDashboard(BuyerRequiredMixin, generic.DetailView):
    """Display the dashboard for users with 'role 0'."""
    model = UserProfile
    template_name = 'user-dashboard/dashboard.html'
    context_object_name = 'buyer_dashboard'

    def get_object(self, queryset=None):
        return get_object_or_404(UserProfile, pk=self.request.user.pk)

# Settings


class BuyerProfileForm(forms.ModelForm):
    """Form for updating buyer's profile."""

    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'email']

# UPDATE settings


@method_decorator(login_required, name='dispatch')
class BuyerSettings(BuyerRequiredMixin, UpdateView):
    """View for updating buyer's settings. Redirect to the same page."""
    model = UserProfile
    form_class = BuyerProfileForm
    template_name = 'user-dashboard/settings.html'
    context_object_name = 'buyer_settings'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        messages.success(self.request, 'Your settings has been updated!')
        return self.request.path

# DELETE Buyer/User Account


@method_decorator(login_required, name='dispatch')
class BuyerDelete(BuyerRequiredMixin, DeleteView):
    """View for deleting the buyer/user profile."""
    model = UserProfile
    template_name = 'user-dashboard/user_delete.html'

    allowed_roles = [0]

    def get_object(self, queryset=None):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        logout(request)
        return response

    def get_success_url(self):
        messages.success(self.request, 'Your account has been deleted!')
        return reverse_lazy('account_login')

# PASSWORD Change


class BuyerPasswordChangeForm(PasswordChangeForm):
    """Form for changing the buyer's password."""

    class Meta:
        fields = ['old_password', 'new_password1', 'new_password2']


@method_decorator(login_required, name='dispatch')
class BuyerPasswordChange(BuyerRequiredMixin, PasswordChangeView):
    """View for changing the buyer's password. Redirect to the same page."""
    template_name = 'user-dashboard/password_change.html'
    form_class = BuyerPasswordChangeForm
    context_object_name = 'buyer_change_password'

    def get_success_url(self):
        messages.success(self.request, 'Your password has changed!')
        return self.request.path


@method_decorator(login_required, name='dispatch')
class BuyerRole(BuyerDashboard):
    """Redender view for role info display"""
    template_name = 'user-dashboard/role.html'
