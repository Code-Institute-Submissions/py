from allauth.account.models import EmailAddress
from decimal import Decimal
from django.shortcuts import get_object_or_404, redirect
from product_service.models import (Product, Service)
from django_plexosoft.settings import (GRAND_DISCOUNT_THRESHOLD,
                                       GRAND_DISCOUNT_PERCENTAGE,

                                       NORMAL_DISCOUNT_THRESHOLD,
                                       NORMAL_DISCOUNT_PERCENTAGE)


def get_verified_email(request):
    """
    Global context processor for EmailAddress model
    """
    if request.user.is_authenticated:
        try:
            email_object = EmailAddress.objects.get(user=request.user)
            if email_object.verified:
                return {'get_verified_email': email_object}
        except EmailAddress.DoesNotExist:
            pass
    return {'get_verified_email': None}


def service_product_bag_content(request):
    """
    Global context processor for service_product_bag_content
    """
    bag_items = []
    total = 0
    product_count = 0
    current_grand_delta = 0
    to_grand_delta = 0
    product_bag = request.session.get('product_bag', {})
    service_bag = request.session.get('service_bag', {})

    if product_bag:
        for product_id, item_data in product_bag.items():
            # product_id is the key and item_data is
            # the dictionary for each product
            quantity = item_data['quantity']
            product = get_object_or_404(Product, pk=product_id)
            product.price = Decimal(product.price)

            total += quantity * product.price
            product_count += quantity
            bag_items.append({
                "product_id": product_id,
                "quantity": quantity,
                "product": product,
            })
    elif service_bag:
        print('service_bag')

    if total < GRAND_DISCOUNT_THRESHOLD:
        discount = total * Decimal(NORMAL_DISCOUNT_PERCENTAGE/100)
        to_grand_delta = GRAND_DISCOUNT_THRESHOLD - total
    else:
        discount = total * Decimal(GRAND_DISCOUNT_PERCENTAGE/100)
        current_grand_delta = total - GRAND_DISCOUNT_THRESHOLD

    grand_total = total - discount

    context = {
        'bag_items': bag_items,
        'total': total,
        'grand_total': grand_total,
        'product_count': product_count,
        'discount': discount,
        'to_grand_delta': to_grand_delta,
        'current_grand_delta': current_grand_delta,
        'grand_discount': GRAND_DISCOUNT_PERCENTAGE,
        'normal_discount': NORMAL_DISCOUNT_PERCENTAGE, }

    return context
