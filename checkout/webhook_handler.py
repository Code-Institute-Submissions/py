from django.http import HttpResponse


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
        return HttpResponse(
            content=f'Unknown webhook received {event["type"]}',
            status=200
        )

    def event_handler_success(self, event):
        """Handle success webhook events"""
        return HttpResponse(
            content=f'Success webhook received {event["type"]}',
            status=200
        )

    def event_handler_failure(self, event):
        """Handle failure webhook events"""
        return HttpResponse(
            content=f'Failure webhook received {event["type"]}',
            status=200
        )
