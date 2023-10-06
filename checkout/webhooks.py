from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import stripe
from .webhook_handler import StripeWebhookHandler
from django.conf import settings
from django.http import HttpResponse
import os

stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
endpoint_secret = os.environ.get('STRIPE_ENDPOINT_SECRET_KEY')


@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhookView(View):
    http_method_names = ['post']  # Allow only POST method

    def post(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        event = None

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except ValueError as e:
            print(f'Error parsing payload: {e}')
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:
            print(f'Error verifying webhook signature: {e}')
            return HttpResponse(status=400)
        except Exception as e:
            return HttpResponse(content=e, status=400)

        # Set up a webhook handler
        handler = StripeWebhookHandler(request)

        # Map webhook events to relevant handler functions
        event_map = {
            'payment_intent.succeeded': handler.event_handler_success,
            'payment_intent.payment_failed': handler.event_handler_failure,
            'payment_intent.payment_canceled': handler.event_handler_failure,
            'checkout.session.completed':
            handler.event_handler_session_completed,
        }

        # Get the webhook type from Stripe
        event_type = event['type']

        # If there's a handler for it, get it from the event map
        # Use the generic one by default
        event_handler = event_map.get(event_type, handler.event_handler)

        # Call the event handler with the event
        response = event_handler(event)
        return response
