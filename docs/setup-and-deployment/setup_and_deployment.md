1. pip3 install 'django<4' gunicorn psycopg2
2. pip3 freeze requirements.txt OR pip3 freeze > requirements.txt
3. django-admin startproject djangopost .
4. python3 manage.py startapp blog
    add to settings.py INSTALLED_APPS
5. touch .gitignore
    Add:
    *.sqllite3
    *.pyc
6. pip3 install cloudinary (not necessary)
7. pip3 install django-cloudinary-storage (not necessary)
- pip3 uninstall cloudinary
- pip3 uninstall django-cloudinary-storage
8. pip3 install dj_database_url
9. pip3 freeze requirements.txt OR pip3 freeze > requirements.txt
10. python3 manage.py makemigrations --dry-run
11. python3 manage.py migrate --plan
12. python3 manage.py migrate
13. python3 manage.py createsuperuser
14. git status
15. git remote -v
16. pip show django | grep Version OR ls ../.pip-modules/lib
17. pip3 install django-allauth==0.54.0
18. Allauth settings:
    AUTHENTICATION_BACKENDS = [
        # Needed to login by username in Django admin, regardless of `allauth`
        'django.contrib.auth.backends.ModelBackend',

        # `allauth` specific authentication methods, such as login by e-mail
        'allauth.account.auth_backends.AuthenticationBackend',
    ]

    SITE_ID = 1  # for social media callback

    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
    ACCOUNT_EMAIL_REQUIRED = True
    ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
    ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE = True
    ACCOUNT_USERNAME_MIN_LENGTH = 4
    LOGIN_URL = '/account/login/'
    LOGIN_REDIRECT_URL = '/'

    `'django.template.context_processors.request',`

        INSTALLED_APPS = [
        'django.contrib.sites',
        'allauth',
        'allauth.account',
        'allauth.socialaccount',
    ]
19. mkdir templates
20. mkdir templates/allauth
21. cp -r ../.pip-modules/lib/python3.8/site-packages/allauth/templates/* ./templates/allauth/ 
22. mkdir static
23. mkdir media
24. mkdir static/css
    On settings.py:
    STATIC_URL = '/static/'

    STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

    MEDIA_URL = '/media/'

    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
25. curl https://cli-assets.heroku.com/install.sh | sh
26. heroku login -i
27. heroku create plexosoft
28. create db on ElephantSQL
29. touch env.py
os.environ["DATABASE_URL"] = "<copiedURL>"
os.environ["SECRET_KEY"]="my_super^secret@key"
os.environ["IN_DEVELOPMENT"] = "True"

then in settings.py:

import os
import dj_database_url
if os.path.isfile('env.py'):
    import env

AND:
IN_DEVELOPMENT = os.environ.get('IN_DEVELOPMENT', False)
DEBUG = IN_DEVELOPMENT

if IN_DEVELOPMENT:
    ALLOWED_HOSTS = ['8000-plexoio-py-om3gwfq21br.ws-eu104.gitpod.io',]
else:
    ALLOWED_HOSTS = [os.environ.get('HEROKU_HOSTNAME'),]

    
if IN_DEVELOPMENT:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': dj_database_url.parse(os.environ.get("DATABASE_URL"))
    }
30. Set up Heroku variables:
DATABASE_URL
PORT = 8000
SECRET_KEY
31. heroku config:set DISABLE_COLLECTSTATIC=1
32. In heroku config vars add:
HEROKU_HOSTNAME