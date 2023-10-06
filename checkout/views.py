# Python standard library imports
import os
import json

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


class CacheCheckoutDataView(View):
    """
    This view handles POST requests to cache checkout data for Stripe.

    It receives the client_secret and save_info variables from the client-side
    after a Stripe checkout session is initiated. It then modifies the corresponding
    Stripe PaymentIntent to include additional metadata such as the current shopping bag,
    the user's preference for saving information, and the username.

    This metadata is stored with the Stripe PaymentIntent for record-keeping and
    possibly for future transaction-related logic.

    Written by Frank Arellano & proofread by ChatGPT4
    """
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        try:
            pid = request.POST.get('client_secret').split('_secret')[0]
            stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
            stripe.PaymentIntent.modify(pid, metadata={
                'bag': json.dumps(request.session.get('item_bag', {})),
                'save_info': request.POST.get('save_info'),
                'username': request.user,
            })

            if 'item_bag' in request.session:
                # Delete() bag after order creation & success message
                del request.session['item_bag']
            return JsonResponse({'status': 'success'}, status=200)
        except Exception as e:
            messages.error(request, ('Sorry, your payment cannot be '
                                     'processed right now. Please try '
                                     'again later.'))
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


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


class CheckoutSuccess(TemplateView):
    """
    This view handles the success page displayed to the user after a
    successful checkout.

    Attributes:
        - stripe_public_key: The public key used for Stripe transactions.
        - client_secret: The client secret of the Stripe PaymentIntent.
        - session_id: The session ID of the Stripe checkout session.
        - save_info: Indicates if the user wants to save their information for
        future purchases.
        - order: The Order object associated with the current transaction.
        - download_password: The password to download a digital good,
        if applicable.

    Methods:
        - get(): Executes the main logic for populating variables and creating
        Stripe PaymentIntent and checkout session.
            1. Fetches the current shopping bag's total amount and item count.
            2. Generates dynamic URLs for Stripe's success and cancel actions.
            3. Creates a new Stripe PaymentIntent with the total amount.
            4. Initializes a new Stripe checkout session with line items and
            URLs.
            5. Associates the order with the user's profile if the user is
            authenticated.
            6. Attaches any saved 'download_password' to the session.

        - get_context_data(): Populates context data for rendering the
        template. Adds stripe_public_key, client_secret, session_id,
        save_info, order, and download_password to the context.
    """
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

        # # Generate dynamic success URL
        # scheme = request.scheme  # http or https
        # host = request.get_host()  # localhost:8000 or your domain
        # success_url = f"{scheme}://{host}/webhook/"

        payment_intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency='eur',
        )

        self.client_secret = payment_intent['client_secret']

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
            success_url='https://8000-plexoio-py-om3gwfq21br.ws-eu105.gitpod.io/',
            cancel_url='http://localhost:8000/cancel/',    # Update with your cancel URL
        )

        self.session_id = session.id

        self.save_info = request.session.get('save_info')

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

        messages.success(request, f'Order created, \
            You will be redirected after 5 seconds!')
        self.order = order

        self.download_password = request.session.get('download_password')
        return super().get(request)

    def get_context_data(self, **kwargs):
        # Retrieve the password from the session variable

        context = super().get_context_data(**kwargs)
        context['save_info'] = self.save_info
        context['client_secret'] = self.client_secret
        context['order'] = self.order
        context['session_id'] = self.session_id
        context['stripe_public_key'] = self.stripe_public_key
        context['password'] = self.download_password
        return context
