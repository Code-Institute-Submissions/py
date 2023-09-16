from django.shortcuts import render

from django.views import View, generic

from product_service.views import Product


class ShoppingBagView(generic.ListView):
    model = Product
    template_name = 'bag/bag.html'
    context_object_name = 'products'

    def get_queryset(self):
        """ Return product instances ordered by creation date."""
        return Product.objects.order_by('-created_on')
