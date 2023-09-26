from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
from .forms import OrderForm
from .models import Order
import os
from product_service.models import (Product, Service)
from homepage.models import UserProfile


class Checkout(TemplateView):
    template_name = 'checkout/checkout.html'

    def get(self, request, *args, **kwargs):
        self.stripe_public_key = os.environ.get('STRIPE_PUBLIC_KEY')
        bag = request.session.get('item_bag', {})
        if not bag:
            messages.error(request, 'Your bag is empty!')
            return redirect(reverse('bag_page'))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['order_form'] = OrderForm(request=self.request)
        context['stripe_public_key'] = self.stripe_public_key
        return context


class CheckoutSuccess(TemplateView):
    template_name = 'checkout/success.html'

    def get(self, request, order_number):
        save_info = request.session.get('save_info')
        order = get_object_or_404(Order, order_number=order_number)
        if request.user.is_authenticated:
            profile = UserProfile.objects.get(username=request.user)
            # Attach the user's profile to the order
            order.user_profile = profile
            order.save()

            # # Save the user's info
            # if save_info:
            #     profile_data = {
            #         'default_phone_number': order.phone_number,
            #     }
            #     user_profile_form = UserProfileForm(profile_data, instance=profile)
            #     if user_profile_form.is_valid():
            #         user_profile_form.save()

        messages.success(request, f'Order successfully processed! \
            Your order number is {order_number}. A confirmation \
            email will be sent to {order.email}.')
        self.order = order
        if 'item_bag' in request.session:
            del request.session['item_bag']
        return super().get(request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = self.order
        return context
