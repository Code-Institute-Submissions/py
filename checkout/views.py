# Third-party library imports (Django)
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView

# Application-specific imports
from .forms import OrderForm
from .models import Order


class Checkout(TemplateView):
    """
    Handles the checkout page, where the user sees the final order details.

    Attributes:
        template_name (str): The name of the template to be rendered.

    Methods:
        get(): Handles GET requests for the checkout page.
            - Checks user authentication.
            - Redirects to the bag page if the bag is empty.

        get_context_data(): Populates additional context data for rendering
        the template.
            - Adds the 'order_form' to the context.
    """
    template_name = 'checkout/general_checkout.html'

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests.
        Checks if the user is authenticated and if the bag is empty.
        """

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
        """
        Populates additional context for rendering the template.
        """
        context = super().get_context_data(**kwargs)
        context['order_form'] = OrderForm(request=self.request)
        return context


class CheckoutSuccess(TemplateView):
    """
    Handles the checkout success page, displayed after a payment,
    when successful.

    Attributes:
        template_name (str): The name of the template to be rendered.
        username (str): The username retrieved from the session.
        order_number (str): The order number retrieved from the session.

    Methods:
        get(request, *args, **kwargs): Handles GET requests for the
        checkout success page.
            - Retrieves username and order number from the session.
            - Displays an info message containing the tracking order number.
            - Returns the default GET response from the parent class.

        get_context_data(**kwargs): Populates additional context data for
        rendering the template.
            - Adds 'order_number' and 'username' to the context.
    """
    template_name = 'checkout/success.html'

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests.
        Retrieves username and order number from the session and
        displays an info message.
        """
        self.username = request.session.get('username')
        self.order_number = request.session.get('order_number')
        user_presence = request.user.is_authenticated

        if user_presence or not user_presence:
            messages.info(
                request, f"""Your tracking order is
                <br><strong>{self.order_number}</strong>""")
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Populates additional context for rendering the template.
        Adds 'order_number' and 'username' to the context.
        """
        context = super().get_context_data(**kwargs)
        context['order_number'] = self.order_number
        context['username'] = self.username
        return context


class CheckoutCancel(TemplateView):
    """
    Handles the checkout cancel page, displayed after a payment,
    when unsuccessful.

    Attributes:
        template_name (str): The name of the template to be rendered.
        username (str): The username retrieved from the session.
        order_number (str): The order number retrieved from the session.

    Methods:
        get(request, *args, **kwargs): Handles GET requests for the
        checkout success page.
            - Retrieves username and order number from the session.
            - Displays an info message containing the tracking order number.
            - Returns the default GET response from the parent class.

        get_context_data(**kwargs): Populates additional context data for
        rendering the template.
            - Adds 'order_number' and 'username' to the context.
    """
    template_name = 'checkout/cancel.html'

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests.
        Retrieves username and order number from the session and
        displays an info message.
        """
        self.username = request.session.get('username')
        self.order_number = request.session.get('order_number')
        user_presence = request.user.is_authenticated

        if user_presence or not user_presence:
            messages.info(
                request, f"""Your tracking order is
                <br><strong>{self.order_number}</strong>""")
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Populates additional context for rendering the template.
        Adds 'order_number' and 'username' to the context.
        """
        context = super().get_context_data(**kwargs)
        context['order_number'] = self.order_number
        context['username'] = self.username
        return context
