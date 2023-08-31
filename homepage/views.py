from django.shortcuts import render
from django.views import View, generic
from django.utils import timezone

# Authentication app imports
from allauth.account.views import LoginView, SignupView, LogoutView

# Local Imports
from .forms import CustomLoginForm, CustomSignupForm

# LOGIN, SIGUNUP & LOGOUT


class CustomLoginView(LoginView):
    """Custom login view that redirects users to dashboard after login."""
    form_class = CustomLoginForm
    template_name = 'account/login.html'

#     def get_success_url(self):
#         user_id = self.request.user.id
#         return reverse_lazy('user_dashboard', kwargs={'pk': user_id})


class CustomSignupView(SignupView):
    """Custom signup view ready for adjustments."""
    form_class = CustomSignupForm
    template_name = 'account/signup.html'


# class CustomLogoutView(LogoutView):
#     """Custom logout view ready for adjustments."""
#     template_name = 'account/logout.html'


class homepage(generic.TemplateView):
    template_name = 'home/homepage.html'
