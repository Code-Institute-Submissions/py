# Django built-in imports
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

# Third-party imports
import stripe

# Application-specific imports
from .models import Order
from product_service.utils import _send_confirmation_email


class StripeWebhookHandler:
    """
    This class handles Stripe webhook events and responds accordingly.

    Methods:
        - __init__(self, request):
        Constructor to initialize the 'request' (HttpRequest) attribute.

        - event_handler(self, event):
        Handles generic and unknown webhook events.

        - event_handler_session_completed(self, event):
        Handles the 'checkout.session.completed' webhook event.

        - event_handler_success(self, event):
        Handles webhook events that indicate success.

        - event_handler_failure(self, event):
        Handles webhook events that indicate failure.

        - event_handler_canceled(self, event):
        Handles webhook events that indicate cancellation.
    """

    def __init__(self, request):
        """"
        We use it to assign the request as an attribute of the class
        just in case we need to access any attributes of the
        request coming from stripe somewhere else in the class.

        Args:
            request (HttpRequest): The incoming request from Stripe's webhook.
        """

        self.request = request

    def event_handler(self, event):
        """
        Handle generic, unknown, or unexpected webhook events.

        Args:
            event (stripe.Event): The event data from Stripe.

        Returns:
            HttpResponse: An HTTP response.
        """

        intent = event.data.object
        event_type = event["type"]
        print(f'MY EVENT IS: {event["type"]} (GENERAL)')

        return HttpResponse(
            content=f'Unknown webhook received {event["type"]}',
            status=200
        )

    def event_handler_session_completed(self, event):
        """
        Handle 'checkout.session.completed' events.

        This method copies the metadata from the completed Stripe session and
        attaches it to the final PaymentIntent object for further processing.

        Args:
            event (stripe.Event): The event data from Stripe.

        Returns:
            HttpResponse: An HTTP response.
        """

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
                order.status = 2
                order.save()

                # Send Email
                _send_confirmation_email(self, order)

        return HttpResponse(
            content=f'Unknown webhook received {event["type"]}',
            status=200
        )

    def event_handler_success(self, event):
        """
        Handle success events.

        Args:
            event (stripe.Event): The event data from Stripe.

        Returns:
            HttpResponse: An HTTP response.
        """
        intent = event.data.object
        event_type = event["type"]
        print(f'MY EVENT IS: {event["type"]} (SUCCESS)')

        return HttpResponse(
            content=f'Success webhook received {event["type"]}',
            status=200
        )

    def event_handler_failure(self, event):
        """
        Handle failure events.

        Args:
            event (stripe.Event): The event data from Stripe.

        Returns:
            HttpResponse: An HTTP response.
        """

        intent = event.data.object
        event_type = event["type"]
        print(f'MY EVENT IS: {event["type"]} (FAILURE)')

        return HttpResponse(
            content=f'Failure webhook received {event["type"]}',
            status=200
        )

    def event_handler_canceled(self, event):
        """
        Handle the canceled webhook event.

        This method deletes the associated order from the database
        if the payment intent has been canceled.

        Args:
            event (stripe.Event): The event data from Stripe.

        Returns:
            HttpResponse: An HTTP response.
        """

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
