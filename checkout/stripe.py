# Python standard library imports
import uuid
from urllib.parse import quote

# Third-party library imports (Django)
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import View

# Application-specific imports
from homepage.models import UserProfile
from product_service.models import Product, Service
from product_service.utils import generate_random_password
from .forms import OrderForm
from .models import Order, OrderLineItem, GATEWAY_TYPE


class StripeCheckoutView(View):
    def post(self, request):
        user = None
        bag = request.session.get('item_bag', {})

        form_data = {
            'full_name': request.POST.get('full_name', ''),
            'email': request.POST.get('email', ''),
            'phone_number': request.POST.get('phone_number', ''),
            'gateway': GATEWAY_TYPE[1][0],
        }

        order_form = OrderForm(request, form_data)
        order = order_form.save(commit=False)
        if order_form.is_valid():

            # Generate a random username
            random_uuid = uuid.uuid4()
            username = str(random_uuid).replace("-", "")

            try:
                # Try to get the user based on the email address
                if request.user.is_authenticated:
                    user = UserProfile.objects.get(
                        email=request.user.email)
                else:
                    user = UserProfile.objects.get(email=form_data['email'])
                    messages.info(
                        request, f'''Log in to your account with {order.email}
                        to find your order!''')
            except UserProfile.DoesNotExist:
                user = UserProfile.objects.create_user(
                    username=username, email=form_data['email'])
                password = generate_random_password()
                encoded_password = quote(password)
                request.session['download_password'] = encoded_password
                user.set_password(password)
                user.first_name = form_data['full_name']
                user.save()
                messages.info(
                    request, f'''Your new password <b>{password} </b>
                        has been downloaded!
                        <br> Password also sent to your email.''')

            # Create/get NEW user profile and associate it with the new user
            # IMPORTANT for ORDER assignment
            if user is not None:
                user_profile, created = UserProfile.objects.get_or_create(
                    username=user)
                order.buyer_profile = user_profile

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

            if order.email != user.email:
                messages.error(request, 'Please, use your own email address.')
                return redirect(reverse('checkout_page'))
            else:
                return redirect(reverse('checkout_success', args=[order.order_number]))
        else:
            messages.error(
                request, 'There was an error with your form. Please double-check your information.')
            return redirect(reverse('checkout_failure'))
