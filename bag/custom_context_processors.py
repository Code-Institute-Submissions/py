# Global context processor for EmailAddress model
from decimal import Decimal
from product_service.models import (Product, Service)
from django_plexosoft.settings import (GRAND_DISCOUNT_THRESHOLD,
                                       GRAND_DISCOUNT_PERCENTAGE,

                                       NORMAL_DISCOUNT_THRESHOLD,
                                       NORMAL_DISCOUNT_PERCENTAGE)


def bag_contents(request):
    bag_items = []
    total = 0
    product_count = 0
    current_grand_delta = 0
    to_grand_delta = 0

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
        'product_count': product_count,
        'discount': discount,
        'to_grand_delta': to_grand_delta,
        'current_grand_delta': current_grand_delta,
        'grand_total': grand_total,
        'grand_discount': GRAND_DISCOUNT_PERCENTAGE,
        'normal_discount': NORMAL_DISCOUNT_PERCENTAGE, }

    return context
