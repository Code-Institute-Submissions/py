import stripe
import os
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views import View
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from homepage.custom_context_processors import service_product_bag_content
from django.conf import settings


@method_decorator(csrf_exempt, name='dispatch')
class StripeCheckoutSessionView(TemplateView):
    template_name = 'checkout/stripe/stripe_checkout.html'

    def get(self, request, *args, **kwargs):
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

        print(session)

        self.session_id = session.id
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['session_id'] = self.session_id
        context['stripe_public_key'] = self.stripe_public_key
        return context
