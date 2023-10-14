# Django Imports
from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

# Local Imports
from .models import (UserProfile,
                     Comment,
                     Like,
                     NewsLetter)


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


# User Related
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(NewsLetter, NewsLetterAdmin)
