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


class BuyerRequiredMixin(UserPassesTestMixin):
    """Mixin to check for user role (role 0) for access control."""

    def test_func(self):
        user_profile = self.request.user
        return user_profile and user_profile.role == 0


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


class BuyerSettings(BuyerRequiredMixin, UpdateView):
    """View for updating buyer's settings."""
    model = UserProfile
    form_class = BuyerProfileForm
    template_name = 'user-dashboard/settings.html'
    context_object_name = 'buyer_settings'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        messages.success(self.request, 'Your settings has been updated!')
        return self.request.path
