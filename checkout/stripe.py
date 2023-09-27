import stripe
import os
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, ListView, View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from homepage.custom_context_processors import service_product_bag_content
from django.conf import settings
from product_service.models import (Product, Service)
from .forms import OrderForm
from .models import Order, OrderLineItem


class StripeCheckoutView(View):
    def post(self, request):
        bag = request.session.get('item_bag', {})

        form_data = {
            'full_name': request.POST.get('full_name', ''),
            'email': request.POST.get('email', ''),
            'phone_number': request.POST.get('phone_number', ''),
        }

        order_form = OrderForm(request, form_data)
        if order_form.is_valid():
            order = order_form.save()

            for item_type, item_data in bag.items():
                try:
                    if item_type == 'product':
                        for product_id, product_info in item_data.items():
                            product_quantity = product_info.get('quantity', 0)
                            product = get_object_or_404(Product, pk=product_id)
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=product_quantity,
                            )
                            order_line_item.save()
                except Product.DoesNotExist:
                    messages.error(
                        request, "One of the products in your bag wasn't found in our database. Please call us for assistance.")
                    order.delete()
                    return redirect(reverse('view_bag'))

                try:
                    if item_type == 'service':
                        for service_id, service_info in item_data.items():
                            service_quantity = service_info.get('quantity', 0)
                            service = get_object_or_404(Service, pk=service_id)
                            order_line_item = OrderLineItem(
                                order=order,
                                service=service,
                                quantity=service_quantity,
                            )
                            order_line_item.save()
                except Service.DoesNotExist:
                    messages.error(
                        request, "One of the services in your bag wasn't found in our database. Please call us for assistance.")
                    order.delete()
                    return redirect(reverse('view_bag'))

            # Save the info to the user's profile if all is well
            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success', args=[order.order_number]))
        else:
            messages.error(
                request, 'There was an error with your form. Please double-check your information.')
            # Handle this URL appropriately
            return redirect(reverse('checkout_failure'))


# @method_decorator(csrf_exempt, name='dispatch')
# class StripeCheckoutSessionView(TemplateView):
#     template_name = 'checkout/stripe/stripe_checkout.html'

#     def get(self, request, *args, **kwargs):
#         self.stripe_public_key = os.environ.get('STRIPE_PUBLIC_KEY')
#         stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

#         current_bag = service_product_bag_content(request)
#         total = current_bag['grand_total']
#         stripe_total = round(total * 100)
#         stripe_quantity = current_bag['item_count']

#         if not self.stripe_public_key:
#             messages.warning(request, '''
#                 STRIPE: Public key not provided!''')

#         session = stripe.checkout.Session.create(
#             payment_method_types=['card'],
#             line_items=[
#                 {
#                     'price_data': {
#                         'currency': settings.STRIPE_CURRENCY,
#                         'product_data': {
#                             'name': 'Plexosoft (Products & Services)',
#                         },
#                         'unit_amount': stripe_total,
#                     },
#                     'quantity': 1,
#                 }
#             ],
#             mode='payment',
#             success_url='http://localhost:8000/success/',  # Update with your success URL
#             cancel_url='http://localhost:8000/cancel/',    # Update with your cancel URL
#         )

#         self.session_id = session.id
#         return super().get(request, *args, **kwargs)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['session_id'] = self.session_id
#         context['stripe_public_key'] = self.stripe_public_key
#         return context
