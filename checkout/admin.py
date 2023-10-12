from django.contrib import admin
from .models import Order, OrderLineItem


class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInline,)

    readonly_fields = ('order_number', 'date', 'order_total',
                       'grand_total', 'stripe_pid')

    fields = ('status', 'order_number', 'buyer_profile', 'date', 'full_name',
              'country', 'email', 'phone_number', 'order_total', 'grand_total',
              'stripe_pid')

    list_display = ('order_number', 'buyer_profile', 'date', 'full_name',
                    'order_total', 'grand_total', 'status',)

    list_filter = ('status', 'country',)

    ordering = ('-date',)


admin.site.register(Order, OrderAdmin)
