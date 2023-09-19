# Django Imports
from django.shortcuts import render, redirect, reverse, HttpResponse
from django.http import HttpResponseServerError
from django.views.generic import View, ListView
from django.contrib import messages
# Python
import logging
# Local Imports
from product_service.views import Product

logger = logging.getLogger(__name__)

# PRODUCT in Cart

# CREATE & READ Product instances in the cart


class ProductAddToCartMixin:
    def add_to_cart(self, product_id):
        """ Add-to-cart method in this module for scalability"""
        try:
            product = Product.objects.filter(status=2).get(id=product_id)
            return product
        except Product.DoesNotExist:
            return False


class ProductAddToCartView(View, ProductAddToCartMixin):
    ''' Independent Add to Cart view for products'''

    def post(self, request, product_id):
        """ Get POST parameters and create session.
        Remember to use "if product_id: request.session.clear()" to clear
        the session when developing."""
        try:
            quantity = int(request.POST.get('quantity'))
            redirect_url = request.POST.get('redirect_url')
            product_bag = request.session.get('product_bag', {})
            product = self.add_to_cart(product_id)
            title = product.title

            if product_id in list(product_bag.keys()):
                product_bag[product_id]['quantity'] += quantity
            else:
                product_bag[product_id] = {
                    'title': title,
                    'quantity': quantity,
                }

            request.session['product_bag'] = product_bag

            messages.success(
                request, f'''You have added
                <strong>{product_bag[product_id]['quantity']}</strong> products
                for <strong>{product_bag[product_id]['title']}</strong>
                in the cart!'''
            )

            return redirect(redirect_url)
        except KeyError:
            messages.error(
                request, '''Data not found in your cart!''')
            return redirect(reverse('bag_page'))
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            messages.error(request, 'An error has occurred!')
            return redirect(reverse('bag_page'))


class ProductShoppingCartView(ListView, ProductAddToCartMixin):
    model = Product
    template_name = 'bag/bag.html'

# UPDATE Product instances in the cart


class UpdateProductCartView(View):
    ''' Update Product instance in the cart'''

    def post(self, request, product_id):
        """ Get POST parameters and update session."""
        try:
            product_bag = request.session.get('product_bag', {})
            new_quantity = int(request.POST.get('quantity'))
            old_quantity = product_bag[product_id]['quantity']

            if new_quantity > 0 and new_quantity <= 100:
                if new_quantity >= old_quantity:
                    quantity_difference = new_quantity - old_quantity
                    product_bag[product_id]['quantity'] += quantity_difference
                elif new_quantity <= old_quantity:
                    quantity_difference = old_quantity - new_quantity
                    product_bag[product_id]['quantity'] -= quantity_difference
            else:
                product_bag.pop(product_id)
                messages.error(
                    request, '''Quantity must be greater than
                    0 and cannot exceed 100!''')

            request.session['product_bag'] = product_bag

            messages.success(
                request, f'''You have
                <strong>{product_bag[product_id]['quantity']}</strong> products
                for <strong>{product_bag[product_id]['title']}</strong>
                in the cart!'''
            )

            return redirect(reverse('bag_page'))
        except KeyError:
            messages.error(
                request, '''Bag, product ID or its data
                not found in your cart!''')
            return redirect(reverse('bag_page'))
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            messages.error(request, 'Quantity field cannot be empty')
            return redirect(reverse('bag_page'))

# DELETE Product instances in the cart


class DeleteProductCartView(View):
    ''' Delete Product instance from cart '''

    def post(self, request, product_id):
        try:
            product_bag = request.session.get('product_bag', {})

            if product_id and product_bag:
                messages.success(
                    request, f'''You have deleted
                    <strong>{product_bag[product_id]['title']}</strong>
                    from the cart successfully!'''
                )
                product_bag.pop(product_id)
            else:
                messages.error(
                    request, '''Product not found in your cart!''')

            request.session['product_bag'] = product_bag

            return redirect(reverse('bag_page'))
        except KeyError:
            messages.error(
                request, '''Data not found in your cart!''')
            return redirect(reverse('bag_page'))

        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            messages.error(request, 'An error has occurred!')
            return redirect(reverse('bag_page'))
