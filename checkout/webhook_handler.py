from django.http import HttpResponse, HttpRequest
from django.contrib.messages.storage.fallback import FallbackStorage
import json
import stripe
from .models import Order
from django.shortcuts import get_object_or_404


class StripeWebhookHandler:
    """
    Handling responses from Stripe payments
    """

    def __init__(self, request):
        '''We use it to assign the request as an attribute of the class
        just in case we need to access any attributes of the
        request coming from stripe somewhere else in the class.'''
        self.request = request

    def event_handler(self, event):
        """Handle webhook events (generic, unknown, unexpected)"""
        intent = event.data.object
        print(f'MY EVENT IS: {event["type"]} (GENERAL)')

        return HttpResponse(
            content=f'Unknown webhook received {event["type"]}',
            status=200
        )

    def event_handler_session_completed(self, event):
        """Handle webhook when session event completed.
        It copies the Metadata from the session and paste it
        in the final paymente intent object for further use."""
        intent = event.data.object
        event_type = event["type"]
        print(f'MY EVENT IS: {event["type"]} (COMPLETED)')

        metadata = intent.get('metadata', {})

        order_number = metadata.get('order_number', {})

        if event_type == "checkout.session.completed":
            payment_intent_id = intent['payment_intent']
            payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)

            # Copy metadata from Session to PaymentIntent object
            stripe.PaymentIntent.modify(
                payment_intent_id,
                metadata=intent.get('metadata', {})
            )

            order = get_object_or_404(Order, order_number=order_number)
            if order:
                order.stripe_pid = payment_intent_id
                order.save()

        return HttpResponse(
            content=f'Unknown webhook received {event["type"]}',
            status=200
        )

    def event_handler_success(self, event):
        """Handle success webhook events"""
        intent = event.data.object
        print(f'MY EVENT IS: {event["type"]} (SUCCESS)')

        return HttpResponse(
            content=f'Success webhook received {event["type"]}',
            status=200
        )

    def event_handler_failure(self, event):
        """Handle failure webhook events"""
        intent = event.data.object
        print(f'MY EVENT IS: {event["type"]} (FAILURE)')

        return HttpResponse(
            content=f'Failure webhook received {event["type"]}',
            status=200
        )

    def event_handler_canceled(self, event):
        """Handle canceled webhook events"""
        intent = event.data.object
        event_type = event["type"]
        print(f'MY EVENT IS: {event["type"]} (CANCELED)')

        if event_type == "payment_intent.payment_canceled":
            payment_intent_id = intent['payment_intent']
            order = get_object_or_404(Order, stripe_pid=payment_intent_id)
            if order:
                order.delete()

        return HttpResponse(
            content=f'Failure webhook received {event["type"]}',
            status=200
        )
