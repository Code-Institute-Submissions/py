# Django Imports
from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

# Local Imports
from .models import (UserProfile,
                     Comment,
                     Like,
                     NewsLetter)
from product_service.models import (CodeType,
                                    ServiceType,
                                    Category,
                                    Product,
                                    Service,
                                    Download,)

from admin_dashboard.models import OrderDeletionRecord


class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'role',
        'type',
        'status',
    )

    list_filter = ('role', 'type', 'status')
    search_fields = ['username', 'email', 'role', 'type', 'status']

    ordering = ('username',)


class CommentAdmin(SummernoteModelAdmin):
    list_display = (
        'writer',
        'product',
        'service',
        'comment',
        'created_on',
        'status',
    )

    list_filter = ('status', 'product', 'service', 'created_on')
    search_fields = ['comment', 'created_on']

    summernote_fields = ('comment')

    ordering = ('-created_on',)


class LikeAdmin(admin.ModelAdmin):
    list_display = (
        'liker',
        'product',
        'service',
        'created_on',
        'status',
    )

    list_filter = ('status', 'product', 'service', 'created_on')
    search_fields = ['created_on', 'status']

    ordering = ('-created_on',)


class NewsLetterAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'excerpt',
        'created_on',
    )
    list_filter = ('created_on',)

    ordering = ('-created_on',)


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


class OrderDeletionRecordAdmin(admin.ModelAdmin):
    list_display = (
        'initiated_by',
        'timestamp',
    )

    list_filter = ('timestamp',)
    search_fields = ['timestamp',]

    ordering = ('-timestamp',)


# User Related
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(NewsLetter, NewsLetterAdmin)

# Product & Service & Order related
admin.site.register(CodeType)
admin.site.register(ServiceType)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Download, DownloadAdmin)
admin.site.register(OrderDeletionRecord, OrderDeletionRecordAdmin)
