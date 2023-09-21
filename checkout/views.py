from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
from .forms import OrderForm


class Checkout(TemplateView):
    template_name = 'checkout/checkout.html'

    def get(self, request):
        bag = request.session.get('bag', {})
        if not bag:
            messages.error(request, 'Your bag is empty!')
            return redirect(reverse('bag_page'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['order_form'] = OrderForm()
        return context
