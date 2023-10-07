# Third-party library imports (Django)
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView

# Application-specific imports
from .forms import OrderForm
from .models import Order


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
