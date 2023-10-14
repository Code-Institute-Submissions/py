# Python standard library imports
import uuid
import os
import json
import time
from urllib.parse import quote

# Third-party library imports (Django and Stripe)
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import View, TemplateView
from django.views.decorators.http import require_POST
from django.http import JsonResponse
import stripe

# Application-specific imports
from homepage.models import UserProfile
from homepage.custom_context_processors import service_product_bag_content
from product_service.models import Product, Service
from product_service.utils import (generate_random_password,
                                   _send_password_email)
from .forms import OrderForm
from .models import Order, OrderLineItem, GATEWAY_TYPE


class StripeCheckoutView(View):
    def post(self, request):
        user = None
        bag = request.session.get('item_bag', {})

        form_data = {
            'full_name': request.POST.get('full_name', ''),
            'country': request.POST.get('country', ''),
            'email': request.POST.get('email', ''),
            'phone_number': request.POST.get('phone_number', ''),
            'gateway': GATEWAY_TYPE[1][0],
        }

        order_form = OrderForm(request, form_data)
        order = order_form.save(commit=False)
        if order_form.is_valid():

            # Generate a random username
            random_uuid = uuid.uuid4()
            username = str(random_uuid).replace("-", "")

            try:
                # Try to get the user based on the email address
                if request.user.is_authenticated:
                    user = UserProfile.objects.get(
                        email=request.user.email)
                else:
                    user = UserProfile.objects.get(email=form_data['email'])
                    messages.info(
                        request, f'''Log in to your account with {order.email}
                        to find your order!''')
            except UserProfile.DoesNotExist:
                user = UserProfile.objects.create_user(
                    username=username, email=form_data['email'])
                password = generate_random_password()
                encoded_password = quote(password)
                request.session['download_password'] = encoded_password
                user.set_password(password)
                user.first_name = form_data['full_name']
                user.save()
                _send_password_email(self, user, password)
                messages.info(
                    request, f'''Your new password <b>{password} </b>
                        has been downloaded!
                        <br> Password also sent to your email.''')

            # Create/get NEW user profile and associate it with the new user
            # IMPORTANT for ORDER assignment
            if user is not None:
                user_profile, created = UserProfile.objects.get_or_create(
                    username=user)
                order.buyer_profile = user_profile
                # For further use in stripe work flow
                request.session['save_info'] = 'save-info' in request.POST
                request.session['username'] = user_profile.username
            order = order_form.save()

            # Pass order number to the session
            request.session['order_number'] = order.order_number

            # Start adding to Order_line_item
            for item_type, item_data in bag.items():
                try:
                    if item_type == 'product':
                        for product_id, product_info in item_data.items():
                            product_quantity = product_info.get('quantity', 0)
                            product = get_object_or_404(Product, pk=product_id)
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=product_quantity,
                            )
                            order_line_item.save()
                except Product.DoesNotExist:
                    messages.error(
                        request, "One of the products in your bag wasn't found in our database. Please call us for assistance.")
                    order.delete()
                    return redirect(reverse('view_bag'))

                try:
                    if item_type == 'service':
                        for service_id, service_info in item_data.items():
                            service_quantity = service_info.get('quantity', 0)
                            service = get_object_or_404(Service, pk=service_id)
                            order_line_item = OrderLineItem(
                                order=order,
                                service=service,
                                quantity=service_quantity,
                            )
                            order_line_item.save()
                except Service.DoesNotExist:
                    messages.error(
                        request, "One of the services in your bag wasn't found in our database. Please call us for assistance.")
                    order.delete()
                    return redirect(reverse('view_bag'))

            if order.email != user.email:
                messages.error(request, 'Please, use your own email address.')
                return redirect(reverse('checkout_page'))
            else:
                return redirect(reverse('stripe_redirect', args=[order.order_number]))
        else:
            messages.error(
                request, 'There was an error with your form. Please double-check your information.')
            return redirect(reverse('checkout_failure'))


class StripeCheckoutRedirect(TemplateView):
    """
    This view handles the success page displayed to the user following a
    successful checkout. Note that this occurs post-checkout but pre-payment
    confirmation. An order is created before the payment, which is subsequently
    marked as completed when the payment is successful. This is achieved
    through Stripe's webhook, specifically the "checkout.session.completed"
    event.

    Attributes:
        - stripe_public_key: The Stripe public key used for transactions.
        - session_id: The unique identifier for the Stripe checkout session.
        - order: The Order model instance related to the current transaction.
        - download_password: A password required for downloading a digital
        good, if applicable.

    Methods:
        - get(request, order_number): Executes the primary logic for populating 
          variables and initializing Stripe's checkout session.
            1. Retrieves the current shopping bag's total amount
            and item count.
            2. Generates a Stripe checkout session with line items and URLs.
            3. Associates the newly created order with the user's profile.
            4. Optionally, attaches a 'download_password' to the session if
            neccessary.

        - get_context_data(**kwargs): Populates context data needed for
        rendering the template. Adds 'stripe_public_key', 'session_id',
        'order', and 'download_password' to the context.

    """
    template_name = 'checkout/stripe/stripe_redirect.html'

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

        # # Generate dynamic success URL
        scheme = request.scheme  # http or https
        host = request.get_host()  # localhost:8000 or your domain
        success_url = f"{scheme}://{host}/checkout/success/"
        cancelled_url = f"{scheme}://{host}/checkout/cancelled/"

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
            # Update with your success URL
            success_url=success_url,
            cancel_url=cancelled_url,
            metadata={
                'bag': json.dumps(request.session.get('item_bag', {})),
                'save_info': request.session.get('save_info'),
                'username': request.session.get('username'),
                'order_number': order_number,
            }
        )

        self.session_id = session.id

        order = get_object_or_404(Order, order_number=order_number)

        # # Save the user's info
        # if save_info:
        #     profile_data = {
        #         'default_phone_number': order.phone_number,
        #     }
        #     user_profile_form = UserProfileForm(profile_data, instance=profile)
        #     if user_profile_form.is_valid():
        #         user_profile_form.save()

        messages.success(request, f'Order created, \
            You will be redirected after 5 seconds!')

        self.order = order

        # Delete() bag after order creation & success message
        if 'item_bag' in request.session:
            del request.session['item_bag']

        self.buyername = request.session.get('username')
        self.download_password = request.session.get('download_password')
        return super().get(request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = self.order
        context['session_id'] = self.session_id
        context['stripe_public_key'] = self.stripe_public_key
        context['buyername'] = self.buyername
        context['password'] = self.download_password
        return context
