from django.shortcuts import render
from django.views import View, generic
from django.utils import timezone

# Authentication app imports
from allauth.account.views import LoginView, SignupView, LogoutView

# Local Imports
from .forms import CustomLoginForm, CustomSignupForm

# LOGIN, SIGUNUP & LOGOUT


class CustomLoginView(LoginView):
    """This view renders our custom login form"""
    form_class = CustomLoginForm
    template_name = 'account/login.html'

#     def get_success_url(self):
#         user_id = self.request.user.id
#         return reverse_lazy('user_dashboard', kwargs={'pk': user_id})


class CustomSignupView(SignupView):
    """This view renders our custom signup form"""
    form_class = CustomSignupForm
    template_name = 'account/signup.html'


# class CustomLogoutView(LogoutView):
#     """Custom logout view ready for adjustments."""
#     template_name = 'account/logout.html'


class homepage(generic.TemplateView):
    template_name = 'home/homepage.html'
