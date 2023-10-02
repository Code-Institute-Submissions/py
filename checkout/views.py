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
import stripe
from homepage.custom_context_processors import service_product_bag_content
from django.conf import settings
from django.contrib.sessions.models import Session


class Checkout(TemplateView):
    template_name = 'checkout/checkout.html'

    def get(self, request, *args, **kwargs):
        bag = request.session.get('item_bag', {})
        if not bag:
            messages.error(request, 'Your bag is empty!')
            return redirect(reverse('bag_page'))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_form'] = OrderForm(request=self.request)
        return context


class CheckoutSuccess(TemplateView):
    template_name = 'checkout/success.html'

    def get(self, request, order_number):

        self.stripe_public_key = os.environ.get('STRIPE_PUBLIC_KEY')
        stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

        current_bag = service_product_bag_content(request)
        total = current_bag['grand_total']
        stripe_total = round(total * 100)
        stripe_quantity = current_bag['item_count']

        if not self.stripe_public_key:
            messages.warning(request, '''
                STRIPE: Public key not provided!''')

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': settings.STRIPE_CURRENCY,
                        'product_data': {
                            'name': 'Plexosoft (Products & Services)',
                        },
                        'unit_amount': stripe_total,
                    },
                    'quantity': 1,
                }
            ],
            mode='payment',
            success_url='http://localhost:8000/success/',  # Update with your success URL
            cancel_url='http://localhost:8000/cancel/',    # Update with your cancel URL
        )

        self.session_id = session.id

        save_info = request.session.get('save_info')
        order = get_object_or_404(Order, order_number=order_number)
        if request.user.is_authenticated:
            profile = UserProfile.objects.get(username=request.user)
            # Attach the user's profile to the order
            order.buyer_profile = profile
            order.save()

            # # Save the user's info
            # if save_info:
            #     profile_data = {
            #         'default_phone_number': order.phone_number,
            #     }
            #     user_profile_form = UserProfileForm(profile_data, instance=profile)
            #     if user_profile_form.is_valid():
            #         user_profile_form.save()

        messages.success(request, f'Order created: <br> \
            Your order number is<br><strong>{order_number}</strong>')
        self.order = order
        if 'item_bag' in request.session:
            # Delete() bag after order creation & success message
            del request.session['item_bag']

        self.download_password = request.session.get('download_password')
        return super().get(request)

    def get_context_data(self, **kwargs):
        # Retrieve the password from the session variable

        context = super().get_context_data(**kwargs)
        context['order'] = self.order
        context['session_id'] = self.session_id
        context['stripe_public_key'] = self.stripe_public_key
        context['password'] = self.download_password
        return context
