# Python standard library imports
import os
import json
import time

# Third-party library imports (Django and Stripe)
from django.conf import settings
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import View, TemplateView
import stripe
from django.views.decorators.http import require_POST
from django.http import JsonResponse

# Application-specific imports
from homepage.models import UserProfile
from homepage.custom_context_processors import service_product_bag_content
from .forms import OrderForm
from .models import Order


class Checkout(TemplateView):
    template_name = 'checkout/checkout.html'

    def get(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            messages.warning(
                request, """The system will create an account for you
                 <strong>after checkout</strong>
                 if you don't already have one.""")

        bag = request.session.get('item_bag', {})
        if not bag:
            messages.error(request, 'Your bag is empty!')
            return redirect(reverse('bag_page'))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_form'] = OrderForm(request=self.request)
        return context
