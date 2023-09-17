from django.shortcuts import render, redirect
from django.views.generic import View, ListView
from django.contrib import messages
from django.http import HttpResponse

from product_service.views import Product


class ProductAddToCartMixin:
    def add_to_cart(self, product_id):
        try:
            product = Product.objects.filter(status=2).get(id=product_id)
            # "add to cart" logic here

            return product
        except Product.DoesNotExist:
            return False


class ProductAddToCartView(View, ProductAddToCartMixin):
    ''' Independent Add to Cart view for products'''

    def post(self, request, product_id):
        ''' Get POST parameters and create session.
        Remember to use "if product_id: request.session.clear()" to clear
        the session when developing.'''

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

        messages.info(
            request, f'''You have <strong>{product_bag[product_id]['quantity']}</strong> products
            for <strong>{product_bag[product_id]['title']}</strong> in the cart!'''
        )

        return redirect(redirect_url)


class ProductShoppingCartView(ListView, ProductAddToCartMixin):
    model = Product
    template_name = 'product_bag/product_bag.html'
    context_object_name = 'products'

    def get_queryset(self):
        """ Return product instances ordered by creation date."""
        return Product.objects.order_by('-created_on')

    def post(self, request, product_id):
        print('placeholder')
