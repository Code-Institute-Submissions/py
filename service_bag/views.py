# Django Imports
from django.shortcuts import render, redirect, reverse, HttpResponse
from django.http import HttpResponseServerError
from django.views.generic import View, ListView
from django.contrib import messages
# Python
import logging
# Local Imports
from product_service.views import Service

logger = logging.getLogger(__name__)

# Service in Cart

# CREATE & READ service instances in the cart


class ServiceAddToCartMixin:
    def add_to_cart(self, service_id):
        """ Add-to-cart method in this module for scalability"""
        try:
            service = Service.objects.filter(status=2).get(id=service_id)
            return service
        except service.DoesNotExist:
            return False


class ServiceAddToCartView(View, ServiceAddToCartMixin):
    ''' Independent Add to Cart view for services'''

    def post(self, request, service_id):
        """ Get POST parameters and create session.
        Remember to use "if service_id: request.session.clear()" to clear
        the session when developing."""
        try:
            quantity = int(request.POST.get('quantity'))
            redirect_url = request.POST.get('redirect_url')
            item_bag = request.session.get('item_bag', {})
            service = self.add_to_cart(service_id)
            title = service.title
            service_id = service.id

            if 'service' not in item_bag:
                item_bag['service'] = {}

            if str(service_id) in item_bag['service']:
                item_bag['service'][str(service_id)]['quantity'] += quantity
            else:
                item_bag['service'][str(service_id)] = {
                    'title': title,
                    'quantity': quantity,
                }
            request.session['item_bag'] = item_bag

            messages.success(
                request, f'''You have added
                <strong>{item_bag['service'][str(service_id)]['quantity']}</strong>
                services for
                <strong>{item_bag['service'][str(service_id)]['title']}</strong>
                in the cart!'''
            )

            return redirect(redirect_url)
        except KeyError as e:
            messages.error(
                request, '''Data not found in your cart!''')
            logger.error(f"KeyError: {str(e)}")
            return redirect(reverse('bag_page'))
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            messages.error(request, 'An error has occurred!')
            return redirect(reverse('bag_page'))

# UPDATE service instances in the cart


class UpdateServiceCartView(View):
    ''' Update service instance in the cart'''

    def post(self, request, service_id):
        """ Get POST parameters and update session."""
        try:
            item_bag = request.session.get('item_bag', {})
            new_quantity = int(request.POST.get('quantity'))
            old_quantity = item_bag['service'][str(service_id)]['quantity']

            if new_quantity > 0 and new_quantity <= 100:
                if new_quantity >= old_quantity:
                    quantity_difference = new_quantity - old_quantity
                    item_bag['service'][str(
                        service_id)]['quantity'] += quantity_difference
                elif new_quantity <= old_quantity:
                    quantity_difference = old_quantity - new_quantity
                    item_bag['service'][str(
                        service_id)]['quantity'] -= quantity_difference
            else:
                item_bag['service'].pop(service_id)
                messages.error(
                    request, '''Quantity must be greater than
                    0 and cannot exceed 100!''')

            request.session['item_bag'] = item_bag

            messages.success(
                request, f'''You have
                <strong>{item_bag['service'][str(service_id)]['quantity']}</strong>
                services for
                <strong>{item_bag['service'][str(service_id)]['title']}</strong>
                in the cart!'''
            )

            return redirect(reverse('bag_page'))
        except KeyError:
            messages.error(
                request, '''Bag, service ID or its data
                not found in your cart!''')
            return redirect(reverse('bag_page'))
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            messages.error(request, 'Quantity field cannot be empty')
            return redirect(reverse('bag_page'))

# DELETE service instances in the cart


class DeleteServiceCartView(View):
    ''' Delete service instance from cart '''

    def post(self, request, service_id):
        try:
            item_bag = request.session.get('item_bag', {})

            if service_id and item_bag:
                messages.success(
                    request, f'''You have deleted
                    <strong>{item_bag['service'][str(service_id)]['title']}</strong>
                    service from the cart successfully!'''
                )
                item_bag['service'].pop(service_id)
            else:
                messages.error(
                    request, '''service not found in your cart!''')

            request.session['item_bag'] = item_bag

            return redirect(reverse('bag_page'))
        except KeyError:
            messages.error(
                request, '''Data not found in your cart!''')
            return redirect(reverse('bag_page'))

        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            messages.error(request, 'An error has occurred!')
            return redirect(reverse('bag_page'))
