from allauth.account.models import EmailAddress
from decimal import Decimal
from django.shortcuts import get_object_or_404
from product_service.models import (Product, Service)
from django_plexosoft.settings import (GRAND_DISCOUNT_THRESHOLD,
                                       GRAND_DISCOUNT_PERCENTAGE,

                                       NORMAL_DISCOUNT_PERCENTAGE,)


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
    item_count = 0
    current_grand_delta = 0
    to_grand_delta = 0
    item_bag = request.session.get('item_bag', {})

    if item_bag:
        for item_type, item_data in item_bag.items():
            if item_type == 'product':
                for product_id, product_info in item_data.items():
                    product_quantity = product_info.get('quantity')
                    item_count += product_quantity
                    product = get_object_or_404(Product, pk=product_id)
                    product.price = Decimal(product.price)
                    total_product = product_quantity * product.price
                    total += total_product

                    # Check if the product is already in bag_items
                    found_product = None
                    for item in bag_items:
                        if 'product' in item and item[
                                'product'].id == product_id:
                            found_product = item
                            break

                    if found_product:
                        # Update existing product
                        found_product['quantity'] += product_quantity
                    else:
                        # Add a new product otherwise
                        product_data = {
                            "product": product,
                            'quantity': product_quantity,
                        }
                        bag_items.append(product_data)

            elif item_type == 'service':

                for service_id, service_info in item_data.items():
                    service_quantity = service_info.get('quantity')
                    item_count += service_quantity
                    service = get_object_or_404(Service, pk=service_id)
                    service.price = Decimal(service.price)
                    total_service = service_quantity * service.price
                    total += total_service

                    # Check if the service is already in bag_items
                    found_service = None
                    for item in bag_items:
                        if 'service' in item and item[
                                'service'].id == service_id:
                            found_service = item
                            break

                    if found_service:
                        # Update existing service
                        found_service['quantity'] += service_quantity
                    else:
                        # Add a new service otherwise
                        service_data = {
                            "service": service,
                            'quantity': service_quantity,
                        }
                        bag_items.append(service_data)

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
        'item_count': item_count,
        'discount': discount,
        'to_grand_delta': to_grand_delta,
        'current_grand_delta': current_grand_delta,
        'grand_discount': GRAND_DISCOUNT_PERCENTAGE,
        'normal_discount': NORMAL_DISCOUNT_PERCENTAGE, }

    return context
