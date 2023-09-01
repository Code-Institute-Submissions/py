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
    """Display the dashboard for users with 'role 1'."""
    model = UserProfile
    template_name = 'admin-dashboard/dashboard.html'
    context_object_name = 'admin_dashboard'

    def get_object(self, queryset=None):
        return get_object_or_404(UserProfile, pk=self.request.user.pk)
