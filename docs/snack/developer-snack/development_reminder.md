## Set Up Django Admin with Summernote

Ensure you have some models in your project. If you don't, you can test these steps later.

### Step 1: Installation
```bash
pip3 install django-summernote
pip3 freeze > requirements.txt
```
This will install django-summernote and then update your project's requirements.txt file.

### Step 2: Update Django Settings
Add `'django_summernote'` to the `INSTALLED_APPS` list in `settings.py`:

```python
INSTALLED_APPS = [
    ...
    'django_summernote',
    ...
]
```

### Step 3: Configure URLs
In your main project's `urls.py`, include the django_summernote URLs:

```python
from django.urls import path, include

urlpatterns = [
    ...
    path('summernote/', include('django_summernote.urls')),
    ...
]
```

### Step 4: Update Admin Configuration
In your `admin.py`, integrate the Summernote editor for the desired model. For this example, we're using the `Post` model:

```python
from django_summernote.admin import SummernoteModelAdmin
from .models import Post

@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)
```

**Note:** You can remove any older registrations of the model that look like:
```python
from .models import Product
admin.site.register(Product)
```
OR 
```python
admin.site.register(Product, ProductAdmin)
```

### Step 5: Database Migrations
If you've made changes to your models, you need to update the database schema. Run:

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

### Step 6: Enhance Admin Features
Enhance your admin view with additional features for better usability:

```python
from django_summernote.admin import SummernoteModelAdmin
from .models import Post

@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('status', 'created_on')
    search_fields = ['title', 'content']
    list_display = ('title', 'slug', 'status', 'created_on')
    summernote_fields = ('content')
    ordering = ('-created_on',)

# OR

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

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Comment, CommentAdmin)
```

With these steps, you'll have Summernote integrated into your Django Admin for the `Post` model, and you've enhanced the admin features for better usability.