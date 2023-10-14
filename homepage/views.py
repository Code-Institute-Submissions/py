from django.shortcuts import render
from django.views.generic import View, ListView
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect, reverse
from django.db.models import Q
from django.contrib import messages
from django.db.models.functions import Lower
from django.db.models import Count
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from operator import attrgetter
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Python
import logging

# Authentication app imports
from allauth.account.views import LoginView, SignupView, LogoutView

# Local Imports
from .forms import (CustomLoginForm,
                    CustomSignupForm,
                    ProductCommentCreationForm,
                    ServiceCommentCreationForm,)
from product_service.models import Product, Service
from checkout.models import Order
from .models import Comment, Like, NewsLetter, UserProfile

logger = logging.getLogger(__name__)

# LOGIN, SIGUNUP & LOGOUT


class CustomLoginView(LoginView):
    """This view renders our custom login form"""
    form_class = CustomLoginForm
    template_name = 'account/login.html'


class CustomSignupView(SignupView):
    """This view renders our custom signup form"""
    form_class = CustomSignupForm
    template_name = 'account/signup.html'


class CustomLogoutView(LogoutView):
    """This view renders our logout page."""
    template_name = 'account/logout.html'

# Cards Display

# Product & Services


class ProductBaseListView(ListView):
    """Base view for listing products based on these conditions."""
    model = Product

    def get_queryset(self):
        """Return products with a status of 2, ordered by creation date."""
        products = Product.objects.filter(status=2).annotate(
            likescount=Count('likes'),
        ).order_by('-created_on')[:3]

        return products


class HomepageProductServiceView(ProductBaseListView):
    """Frontend main page displaying the list of products & services."""
    template_name = 'home/homepage.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        products = list(context['products'][:3])
        services = list(Service.objects.filter(
            status=2).annotate(
                likescount=Count('likes'),
        ).order_by('-created_on')[:3])

        product_single = []
        service_single = []

        combined_list = []

        # 1 product, 1 services, 1 product INTENTION
        if products and services:
            product_single.extend(products[:3])
            service_single.extend(services[:3])

            combined_list.extend(products[:1])
            products = products[2:]

            combined_list.extend(services[:1])
            services = services[3:]

            combined_list.extend(products[:1])
            products = products[1:]

        order_count_combined = {}
        order_count_product = {}
        order_count_service = {}

        for item in combined_list:
            if item.instance == 0:
                order_count = Order.objects.filter(
                    status=2, lineitems__product=item).count()
                order_count_combined[item.title] = order_count
            else:
                order_count = Order.objects.filter(
                    status=2, lineitems__service=item).count()
                order_count_combined[item.title] = order_count

        for item in product_single:
            if item.instance == 0:
                order_count = Order.objects.filter(
                    status=2, lineitems__product=item).count()
                order_count_product[item.title] = order_count

        for item in service_single:
            if item.instance == 1:
                order_count = Order.objects.filter(
                    status=2, lineitems__service=item).count()
                order_count_service[item.title] = order_count

        context['combined_items'] = combined_list
        context['product_single'] = product_single
        context['service_single'] = service_single
        context['order_count_combined'] = order_count_combined
        context['order_count_product'] = order_count_product
        context['order_count_service'] = order_count_service
        return context

# All Product & Services


class AllProductServiceListView(ListView):
    """Dedicated page for displaying list of all products & services and
    instances from the search engine & category implementation."""
    model = Product
    template_name = 'all_product_service/all_product_service.html'
    paginate_by = 6

    # Search Engine logic starts here
    search = None
    searched_items = None

    def get(self, request, *args, **kwargs):
        """
        For the Request Handling.
        """
        # .strip() to remove any accidental whitespace
        self.search = request.GET.get('q', '').strip()

        # Check if search keyword is empty or only consists of whitespaceF
        if not self.search:
            messages.info(
                request, 'Try using our internal search bar!')
            return super().get(request, *args, **kwargs)

        # If search keyword exists, proceed with the search logic
        combined_list = self.combine_products_and_services(
            list(Product.objects.filter(status=2).annotate(
                likescount=Count('likes'),
            ).order_by('-created_on')),
            list(Service.objects.filter(status=2).annotate(
                likescount=Count('likes'),
            ).order_by('-created_on'))
        )

        # Filter the combined list based on the searched keyword
        self.searched_items = [
            item for item in combined_list
            if self.search.lower() in item.title.lower()
            or (item.category and self.search.lower(
            ) in item.category.alt_name.lower())
            or self.search.lower() in item.get_type_display().lower()
            or self.search.lower() in item.description.lower()
        ]

        # Check if searched_items was filled with results
        if not self.searched_items:
            messages.info(request, 'No results found for your search.')

        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        """
        For the View.
        And conditional code if 'searched_items'.
        """
        # # If YES searched_items run this
        if self.searched_items is not None:
            return self.searched_items

        # If NOT searched_items run this
        try:
            products = list(Product.objects.filter(
                status=2).annotate(
                likescount=Count('likes'),
            ).order_by('-created_on'))
            services = list(Service.objects.filter(
                status=2).annotate(
                likescount=Count('likes'),
            ).order_by('-created_on'))

            combined_list = self.combine_products_and_services(
                products, services)
            return combined_list
        except Exception as e:
            logger.error(f"Error fetching products and services: {str(e)}")
            return []

    def get_context_data(self, **kwargs):
        """
        For the template display. Comments are important.
        From here on the code will run based on get_queryset results.
        """
        context = super().get_context_data(**kwargs)

        # Get results
        combined_list = self.get_queryset()

        # Order Counts
        order_counts = {}
        for item in combined_list:
            if item.instance == 0:
                order_count = Order.objects.filter(
                    status=2, lineitems__product=item).count()
                order_counts[item.title] = order_count
            else:
                order_count = Order.objects.filter(
                    status=2, lineitems__service=item).count()
                order_counts[item.title] = order_count

        # Pagination
        paginator = Paginator(combined_list, self.paginate_by)
        page_number = self.request.GET.get('page', 1)

        try:
            page_obj = paginator.page(page_number)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        except PageNotAnInteger:
            page_obj = paginator.page(1)

        # Get unique categories
        unique_categories = list(set([obj.category for obj in page_obj]))

        # Establish template context variables
        context['page_obj'] = page_obj
        context['categories'] = unique_categories
        context['is_paginated'] = len(combined_list) > self.paginate_by
        context['order_count'] = order_counts
        return context

    def combine_products_and_services(self, products, services):
        """
        This function can be called in this class scope with 'self.'.
        No rearranging of the list when using pop() is necessary
        with this approach.
        """
        combined_list = []

        # Convert lists to iterators
        product_iter = iter(products)
        service_iter = iter(services)

        # Flags to check if iterators have more items
        has_more_products = True
        has_more_services = True

        # Combine products and services
        while has_more_products or has_more_services:
            if has_more_products:
                try:
                    combined_list.append(next(product_iter))
                except StopIteration:
                    has_more_products = False

            if has_more_services:
                try:
                    combined_list.append(next(service_iter))
                except StopIteration:
                    has_more_services = False

        return combined_list


# All Product


class AllProductListView(ListView):
    model = Product
    template_name = 'all_product_service/all_product.html'
    paginate_by = 6
    context_object_name = 'product_all'

    def get_queryset(self):
        try:
            return Product.objects.filter(status=2).annotate(
                likescount=Count('likes'),
            ).order_by('-created_on')
        except Exception as e:
            logger.error(f"Error fetching Product instances: {str(e)}")
            messages.error(self.request, 'Error fetching Product instances.')
            return []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        product_all = context[self.context_object_name]

        # Order Counts
        order_counts = {}
        for item in product_all:
            if item.instance == 0:
                order_count = Order.objects.filter(
                    status=2, lineitems__product=item).count()
                order_counts[item.title] = order_count

        unique_categories = list(
            set([product.category for product in product_all]))

        context['categories'] = unique_categories
        context['order_count'] = order_counts
        return context

# All Services


class AllServiceListView(ListView):
    """Dedicated page for displaying list of all service instances."""
    model = Service
    template_name = 'all_product_service/all_service.html'
    paginate_by = 6
    context_object_name = 'service_all'

    def get_queryset(self):
        try:
            return Service.objects.filter(status=2).annotate(
                likescount=Count('likes'),
            ).order_by('-created_on')
        except Exception as e:
            logger.error(f"Error fetching Service instances: {str(e)}")
            messages.error(self.request, 'Error fetching Service instances.')
            return []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        service_all = context[self.context_object_name]

        # Order Counts
        order_counts = {}
        for item in service_all:
            if item.instance == 1:
                order_count = Order.objects.filter(
                    status=2, lineitems__service=item).count()
                order_counts[item.title] = order_count

        unique_categories = list(
            set([service.category for service in service_all]))

        context['categories'] = unique_categories
        context['order_count'] = order_counts
        return context

# Product Single

# Comment Creation View


class ProductCommentListView(ListView):
    model = Comment
    paginate_by = 6
    context_object_name = 'comments_list'

    def get_queryset(self):
        """Return comments with a status of 2 and comments count,
        ordered by creation date."""
        self.get_product(self.request, self.kwargs['slug'])
        comments = Comment.objects.filter(
            status=2, instance=0, product=self.product).order_by('-created_on')
        self.comment_count = Comment.objects.filter(
            status=2, instance=0,
            product=self.product).order_by('-created_on').count()
        if self.request.user.is_authenticated:
            self.user_commented = Comment.objects.filter(
                writer=self.request.user,
                instance=0,
                product=self.product).order_by('-created_on').exists()
        return comments


class SingleProductView(ProductCommentListView):
    """View for listing SINGLE product instances."""
    template_name = 'single_product_service/single_product.html'

    def get_product(self, request, slug):
        queryset = Product.objects.annotate(
            likescount=Count('likes'),
        ).order_by('-created_on')
        self.product = get_object_or_404(queryset, slug=slug)
        self.order_count = Order.objects.filter(
            status=2, lineitems__product=self.product).count()

        # Check if user purchased or not
        if request.user.is_authenticated:
            self.has_purchased = Order.objects.filter(
                buyer_profile=request.user, status=2,
                lineitems__product=self.product).exists()
        else:
            self.has_purchased = False

        # Check if user has liked or not
        if request.user.is_authenticated:
            self.has_liked = Like.objects.filter(
                liker=request.user, status=2,
                product=self.product).exists()
        else:
            self.has_liked = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        self.get_product(self.request, self.kwargs['slug'])

        context['product'] = self.product
        context['order_count'] = self.order_count
        context['has_purchased'] = self.has_purchased
        context['has_liked'] = self.has_liked
        context['user_authenticated'] = self.request.user.is_authenticated
        context['comment_count'] = self.comment_count
        if self.request.user.is_authenticated:
            context['commented'] = self.user_commented

        # Comment Form
        comment_form = ProductCommentCreationForm(
            self.request, initial={'writer': self.request.user,
                                   'product': self.product})
        context['comment_form'] = comment_form

        return context

    def get(self, request, slug, *args, **kwargs):
        return super().get(request, slug, *args, **kwargs)

    def post(self, request, slug, *args, **kwargs):
        self.get_product(request, slug)

        # Comment
        comment_form = ProductCommentCreationForm(request, data=request.POST)
        if 'comment_submit' in request.POST:
            if comment_form.is_valid():
                if request.user.is_authenticated and self.has_purchased:
                    comment_form.instance.writer = request.user
                    comment_form.instance.product = self.product
                    comment_form.save()
                    messages.success(
                        request, '''Your comment has been submitted!
                        <br>Awaiting for approval!''')
                else:
                    messages.error(
                        request, '''You need to log in
                        & purchase a product to comment!''')
            else:
                error_messages = []
                for field, errors in comment_form.errors.items():
                    field_errors = ', '.join(errors)
                    error_messages.append(f"{field}: {field_errors}")

                error_message_str = ', '.join(error_messages)
                messages.error(
                    request, f'Your form is not valid!<br>{error_message_str}')

        # Sperclass method which takes care of calling get_context_data
        # and rendering the template
        return super().get(request, slug, *args, **kwargs)

# Service Single

# Comment Creation View


class ServiceCommentListView(ListView):
    model = Comment
    paginate_by = 6
    context_object_name = 'comments_list'

    def get_queryset(self, **kwargs):
        """Return comments with a status of 2 and comments count,
        ordered by creation date."""
        self.get_service(self.request, self.kwargs['slug'])
        comments = Comment.objects.filter(
            status=2, instance=1, service=self.service).order_by(
                '-created_on')
        self.comment_count = Comment.objects.filter(
            status=2, instance=1, service=self.service).order_by(
                '-created_on').count()
        if self.request.user.is_authenticated:
            self.user_commented = Comment.objects.filter(
                writer=self.request.user,
                instance=1,
                service=self.service).order_by('-created_on').exists()
        return comments


class SingleServiceView(ServiceCommentListView):
    """View for listing SINGLE service instances."""
    template_name = 'single_product_service/single_service.html'

    def get_service(self, request, slug):
        queryset = Service.objects.annotate(
            likescount=Count('likes'),
        ).order_by('-created_on')
        self.service = get_object_or_404(queryset, slug=slug)
        self.order_count = Order.objects.filter(
            status=2, lineitems__service=self.service).count()

        # Check if user purchased or not
        if request.user.is_authenticated:
            self.has_purchased = Order.objects.filter(
                buyer_profile=request.user, status=2,
                lineitems__service=self.service).exists()
        else:
            self.has_purchased = False

        # Check if user has liked or not
        if request.user.is_authenticated:
            self.has_liked = Like.objects.filter(
                liker=request.user, status=2,
                service=self.service).exists()
        else:
            self.has_liked = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        self.get_service(self.request, self.kwargs['slug'])

        context['service'] = self.service
        context['order_count'] = self.order_count
        context['has_purchased'] = self.has_purchased
        context['has_liked'] = self.has_liked
        context['user_authenticated'] = self.request.user.is_authenticated
        context['comment_count'] = self.comment_count
        if self.request.user.is_authenticated:
            context['commented'] = self.user_commented

        # Comment Form
        comment_form = ServiceCommentCreationForm(
            self.request, initial={'writer': self.request.user,
                                   'service': self.service})
        context['comment_form'] = comment_form

        return context

    def get(self, request, slug, *args, **kwargs):
        return super().get(request, slug, *args, **kwargs)

    def post(self, request, slug, *args, **kwargs):
        self.get_service(request, slug)

        # Comment
        comment_form = ServiceCommentCreationForm(request, data=request.POST)
        if 'comment_submit' in request.POST:
            if comment_form.is_valid():
                if request.user.is_authenticated and self.has_purchased:
                    comment_form.instance.writer = request.user
                    comment_form.instance.service = self.service
                    comment_form.instance.instance = 1
                    comment_form.save()
                    messages.success(
                        request, '''Your comment has been submitted!
                        <br>Awaiting for approval!''')
                else:
                    messages.error(
                        request, '''You need to log in
                        & purchase a service to comment!''')
            else:
                error_messages = []
                for field, errors in comment_form.errors.items():
                    field_errors = ', '.join(errors)
                    error_messages.append(f"{field}: {field_errors}")

                error_message_str = ', '.join(error_messages)
                messages.error(
                    request, f'Your form is not valid!<br>{error_message_str}')

        # Sperclass method which takes care of calling get_context_data
        # and rendering the template
        return super().get(request, slug, *args, **kwargs)


class SortedProductServiceListView(ListView):
    '''
    View for sorting products & services
    '''
    model = Product
    template_name = 'sorted_product_service/sorted_product_service.html'
    paginate_by = 6
    context_object_name = 'combined_items'

    def get_queryset(self):
        sortkey = self.request.GET.get('sort', 'created_on')
        direction = self.request.GET.get('direction', 'asc')
        self.sortkey = sortkey
        self.direction = direction

        products = Product.objects.filter(status=2).annotate(
            lower_title=Lower('title'),
            likescount=Count('likes'),
        ).order_by('created_on')

        services = Service.objects.filter(status=2).annotate(
            lower_title=Lower('title'),
            likescount=Count('likes'),
        ).order_by('created_on')

        combined_list = self.combine_products_and_services(
            list(products),
            list(services)
        )

        self.order_counts = {}
        for item in combined_list:
            if item.instance == 0:
                order_count = Order.objects.filter(
                    status=2, lineitems__product=item).count()
                self.order_counts[item.title] = order_count
            else:
                order_count = Order.objects.filter(
                    status=2, lineitems__service=item).count()
                self.order_counts[item.title] = order_count

        try:
            if sortkey == 'title':
                combined_list.sort(key=lambda item: item.title.lower())
            elif sortkey == 'likescount':
                combined_list.sort(key=lambda item: float(item.likescount))
            elif sortkey == 'transactionscount':
                combined_list.sort(
                    key=lambda item: (
                        float(self.order_counts.get(item.title, 0)),
                    )
                )
            elif sortkey == 'price':
                combined_list.sort(key=lambda item: float(item.price))
            elif sortkey == 'category':
                combined_list.sort(
                    key=lambda item: item.category.category_name.lower())
            else:
                combined_list.sort(key=lambda item: item.created_on)

        except Exception as e:
            logger.error(
                f"Error while sorting products and services: {str(e)}")
            messages.error(self.request, 'That was not a valid sorting value.')
            return []

        if direction == 'desc':
            combined_list.reverse()

        return combined_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        combined_list = context['combined_items']

        unique_categories = list(
            set([item.category for item in combined_list]))

        context['sortkey'] = self.sortkey
        context['direction'] = self.direction
        context['categories'] = unique_categories
        context['order_count'] = self.order_counts
        return context

    def combine_products_and_services(self, products, services):
        combined_list = []
        product_iter = iter(products)
        service_iter = iter(services)

        has_more_products = True
        has_more_services = True

        while has_more_products or has_more_services:
            if has_more_products:
                try:
                    combined_list.append(next(product_iter))
                except StopIteration:
                    has_more_products = False

            if has_more_services:
                try:
                    combined_list.append(next(service_iter))
                except StopIteration:
                    has_more_services = False

        return combined_list

# Likes Creation

# Product LIKE


@method_decorator(login_required, name='dispatch')
class ProductLikePost(View):
    """
    Handle the product like functionality.

    This view leverages Django's Class-Based Views and is designed to work with
    AJAX on the frontend. It uses `transaction.atomic()` to ensure
    data integrity during the database operations.

    JsonResponse is used to communicate the result back to the AJAX code
    on the frontend.
    """

    def post(self, request, slug):
        if not request.user.is_authenticated:
            return JsonResponse(
                {'status': 'fail', 'message': 'User not authenticated'}
            )

        product = get_object_or_404(Product, slug=slug)

        existing_like = Like.objects.filter(
            liker=request.user, product=product).first()

        with transaction.atomic():
            if request.user.is_authenticated:
                # If a 'Like' already exists, remove it
                if existing_like:
                    existing_like.delete()
                    messages.success(request, "You've unliked this product!")
                else:
                    # Otherwise, create a new 'Like' record
                    like_instance = Like.objects.create(
                        liker=request.user,
                        product=product,
                        status=2,
                    )
                    product.likes.add(like_instance)
                    messages.success(request, "You've liked this product!")

        return JsonResponse(
            {'status': 'success', 'message': 'Like status updated'})


# Service LIKE

@method_decorator(login_required, name='dispatch')
class ServiceLikePost(View):
    """
    Handle the service like functionality.

    This view leverages Django's Class-Based Views and is designed to work with
    AJAX on the frontend. It uses `transaction.atomic()` to ensure
    data integrity during the database operations.

    JsonResponse is used to communicate the result back to the AJAX code
    on the frontend.
    """

    def post(self, request, slug):
        if not request.user.is_authenticated:
            return JsonResponse(
                {'status': 'fail', 'message': 'User not authenticated'}
            )

        service = get_object_or_404(Service, slug=slug)

        existing_like = Like.objects.filter(
            liker=request.user, service=service).first()

        with transaction.atomic():
            if request.user.is_authenticated:
                # If a 'Like' already exists, remove it
                if existing_like:
                    existing_like.delete()
                    messages.success(request, "You've unliked this service!")
                else:
                    # Otherwise, create a new 'Like' record
                    like_instance = Like.objects.create(
                        liker=request.user,
                        service=service,
                        instance=1,
                        status=2,
                    )
                    service.likes.add(like_instance)
                    messages.success(request, "You've liked this service!")

        return JsonResponse(
            {'status': 'success', 'message': 'Like status updated'})

# Newsletter LIKE


class NewsletterPost(View):
    """
    Handle the newsletter functionality.
    """

    def post(self, request):
        with transaction.atomic():
            # Here 'email' should be the key that you've sent via AJAX
            email = request.POST.get('email')

            existing_newsletter = NewsLetter.objects.filter(
                email=email).exists()

            if not existing_newsletter:
                newsletter_instance = NewsLetter.objects.create(
                    email=email,
                    excerpt='Related to Mailchimp',
                )
            else:
                return JsonResponse(
                    {'status': 'error', 'message': 'Email already exists in our database!'})

        return JsonResponse(
            {'status': 'success', 'message': 'Email added to our internal newsletter!'})

# TERMS & CONDITIONS PAGE


class TermsView(ListView):
    ''' Implemented terms & conditions view ready for adjustments '''
    model = UserProfile
    template_name = "policy_terms/terms_conditions.html"
    context_object_name = 'terms_page'

# PRIVACY POLICY PAGE


class PrivacyView(ListView):
    ''' Implemented privacy policy view ready for adjustments '''
    model = UserProfile
    template_name = "policy_terms/privacy_policy.html"
    context_object_name = 'privacy_page'

# CONTACT FORM


class ContactView(ListView):
    ''' Implemented contact view ready for adjustments '''
    model = UserProfile
    template_name = "faq_contact/contact.html"
    context_object_name = 'contact_form'

# FAQ


class FAQView(ListView):
    ''' Implemented FAQ view ready for adjustments '''
    model = UserProfile
    template_name = "faq_contact/faq.html"
    context_object_name = 'faq_page'
