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
    template_name = 'checkout/checkout.html'

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
