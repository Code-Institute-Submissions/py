from django.contrib import admin
from .models import OrderDeletionRecord
# Register your models here.


class OrderDeletionRecordAdmin(admin.ModelAdmin):
    list_display = (
        'initiated_by',
        'timestamp',
    )

    list_filter = ('timestamp',)
    search_fields = ['timestamp',]

    ordering = ('-timestamp',)


admin.site.register(OrderDeletionRecord, OrderDeletionRecordAdmin)
