from django.shortcuts import render, redirect
from django.views.generic import View, ListView
from django.contrib import messages
from django.http import HttpResponse

from product_service.views import Product


class ProductAddToCartMixin:
    def add_to_cart(self, product_id):
        print('placeholder')


class ProductAddToCartView(View, ProductAddToCartMixin):
    def post(self, request, product_id):
        quantity = int(request.POST.get('quantity'))
        redirect_url = request.POST.get('redirect_url')
        bag = request.session.get('bag', {})

        if product_id in list(bag.keys()):
            bag[product_id] += quantity
        else:
            bag[product_id] = quantity

        request.session['bag'] = bag

        messages.info(
            request, f'You have {bag[product_id]} products in the cart!')
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
