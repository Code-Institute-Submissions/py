import stripe
import os
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views import View
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')


@method_decorator(csrf_exempt, name='dispatch')
class StripeCheckoutSessionView(TemplateView):
    template_name = 'checkout/stripe/stripe_checkout.html'

    def get(self, request, *args, **kwargs):
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'eur',
                        'product_data': {
                            'name': 'Product & Service',
                        },
                        'unit_amount': 2000,
                    },
                    'quantity': 1,
                }
            ],
            mode='payment',
            success_url='http://localhost:8000/success/',  # Update with your success URL
            cancel_url='http://localhost:8000/cancel/',    # Update with your cancel URL
        )

        self.session_id = session.id
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['session_id'] = self.session_id
        context['stripe_public_key'] = os.environ.get('STRIPE_PUBLIC_KEY')
        return context
