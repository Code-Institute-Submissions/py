from django.shortcuts import render, redirect
from django.views.generic import View, ListView
from django.contrib import messages
from django.http import HttpResponse

from product_service.views import Product


class ProductAddToCartMixin:
    def add_to_cart(self, product_id):
        try:
            product = Product.objects.get(id=product_id)
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
        bag = request.session.get('bag', {})
        product = self.add_to_cart(product_id)
        title = product.title

        if product_id in list(bag.keys()):
            bag[product_id] += quantity
        else:
            bag[title] = title
            bag[product_id] = quantity

        request.session['bag'] = bag

        messages.info(
            request, f'''You have <strong>{bag[product_id]}</strong> products
            for <strong>{bag[title]}</strong> in the cart!'''
        )

        return redirect(redirect_url)


class ProductShoppingCartView(ListView, ProductAddToCartMixin):
    model = Product
    template_name = 'bag/bag.html'
    context_object_name = 'products'

    def get_queryset(self):
        """ Return product instances ordered by creation date."""
        return Product.objects.order_by('-created_on')

    def post(self, request, product_id):
        print('placeholder')
