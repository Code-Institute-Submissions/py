# Django Imports
from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

# Local Imports
from .models import (UserProfile,
                     Comment,
                     Like,
                     NewsLetter)
from product_service.models import (Category,
                                    Product,
                                    Service,
                                    Download,
                                    Transaction)


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
    )

    list_filter = ('created_on', 'product', 'service')
    search_fields = ['comment', 'created_on']

    summernote_fields = ('comment')

    ordering = ('-created_on',)


class LikeAdmin(admin.ModelAdmin):
    list_display = (
        'liker',
        'product',
        'service',
        'created_on',
    )

    list_filter = ('product', 'service', 'created_on')
    search_fields = ['created_on']

    ordering = ('liker',)


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
        'product',
        'service',
        'file_url',
        'status',
    )

    list_filter = ('product', 'service', 'status')
    search_fields = ['file_url', 'status']

    ordering = ('product',)


class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'buyer',
        'product',
        'service',
        'sku',
        'price',
        'paid',
        'gateway',
        'timestamp'
    )
    list_filter = ('product', 'service', 'gateway')
    search_fields = ['gateway', 'timestamp']

    ordering = ('-timestamp',)


# User Related
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(NewsLetter, NewsLetterAdmin)

# Product & Service related
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Download, DownloadAdmin)
admin.site.register(Transaction, TransactionAdmin)
