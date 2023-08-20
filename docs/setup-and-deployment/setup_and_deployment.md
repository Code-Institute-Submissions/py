1. pip3 install 'django<4' gunicorn psycopg2
2. pip3 freeze requirements.txt OR pip3 freeze > requirements.txt
3. django-admin startproject djangopost .
4. python3 manage.py startapp blog
    add to settings.py INSTALLED_APPS
5. touch .gitignore
    Add:
    *.sqllite3
    *.pyc
6. pip3 install cloudinary
7. pip3 install django-cloudinary-storage
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