## Set up Django Admin

Make sure you have some models installed, if not test later.

1. pip3 install django-summernote
use `pip3 freeze > requirements.txt `after installation
2. Add 'django_summernote' to the settings.py 'INSTALLED_APPS'
3. Add on main project's urls: 
    path('summernote/'), include('django_summernote.urls'),
4. Add on admin.py:
from .models import Post

@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('content')

instead of:
from .models import.
admin.site.register(Product)
5. Make migrations database was modified if not just run migrate:
`python3 manage.py makemigrations`
`python3 manage.py migrate`