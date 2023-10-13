# Django standard library imports
from django.views import View
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# Third-party library imports
import os
import stripe

# Application-specific imports
from .webhook_handler import StripeWebhookHandler
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

# Initialize Stripe API
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
endpoint_secret = os.environ.get('STRIPE_ENDPOINT_SECRET_KEY')


@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhookView(View):
    """
    View to handle incoming Stripe Webhooks.

    This view is CSRF exempt and only allows POST requests to handle
    Stripe webhook events. The events are then passed to the appropriate
    event handlers for further processing.

    Attributes:
        http_method_names (list): List of allowed HTTP methods.
        Here, only POST is allowed.
    """
    http_method_names = ['post']  # Allow only POST method

    def post(self, request, *args, **kwargs):
        """
        Handle incoming POST request containing Stripe webhook data.

        The method performs the following steps:
        1. Parse and verify the incoming payload and signature from Stripe.
        2. Identify the type of event (e.g., payment succeeded, payment failed)
        3. Dispatch the event to the appropriate handler function
        for further action.

        Args:
            request (HttpRequest): The request object containing
            metadata and payload.

        Returns:
            HttpResponse: An HTTP response indicating the status
            of the operation.
        """
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        event = None

        # For Debugging
        logger.info(f"Received payload: {payload}")
        logger.info(f"Received Stripe signature header: {sig_header}")

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
