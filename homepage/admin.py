from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import UserProfile, Comment, Like, NewsLetter
from product_service.models import Category, Product, Service, Download, Transaction

# @admin.register(Post)
# class PostAdmin(SummernoteModelAdmin):
#     prepopulated_fields = {'slug': ('title',)}
#     list_filter = ('status', 'created_on')
#     search_fields = ['title', 'content']
#     list_display = ('title', 'slug', 'status', 'created_on')
#     summernote_fields = ('content')

#     ordering = ('-created_on',)

admin.site.register(UserProfile)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(NewsLetter)
admin.site.register(Product)
admin.site.register(Transaction)
