from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import (CodeType,
                     ServiceType,
                     Category,
                     Product,
                     Service,
                     Download,)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'category_name',
        'alt_name',
    )


class ProductAdmin(SummernoteModelAdmin):
    list_display = (
        'title',
        'sku',
        'category',
        'type',
        'status',
        'author',
    )

    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('status', 'created_on')
    search_fields = ['title', 'description', 'sku', 'type', 'status']

    summernote_fields = ('description')

    ordering = ('-created_on',)


class ServiceAdmin(SummernoteModelAdmin):
    list_display = (
        'title',
        'sku',
        'category',
        'type',
        'status',
        'author',
    )

    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('status', 'created_on')
    search_fields = ['title', 'description', 'sku', 'type', 'status']

    summernote_fields = ('description')

    ordering = ('-created_on',)


class DownloadAdmin(admin.ModelAdmin):
    list_display = (
        'file_name',
        'product',
        'service',
        'status',
        'download_token',
        'created_on',
    )

    list_filter = ('status',)
    search_fields = ['file_name', 'file_url', 'status']

    ordering = ('file_name',)


# Product & Service & Order related
admin.site.register(CodeType)
admin.site.register(ServiceType)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Download, DownloadAdmin)
