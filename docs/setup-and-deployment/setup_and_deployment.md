## Extended Version

**1. Initial Setup:**

- Install necessary packages:
  ```bash
  pip3 install 'django<4' gunicorn psycopg2
  ```

- Freeze and save your dependencies:
  ```bash
  pip3 freeze > requirements.txt
  ```

- Start your Django project and app:
  ```bash
  django-admin startproject djangopost .
  python3 manage.py startapp blog
  ```

  *Note: Remember to add your app to the `INSTALLED_APPS` list in `settings.py`.*

**2. Version Control with Git:**

- Create a `.gitignore` file:
  ```bash
  touch .gitignore
  ```

  Then add the following lines to `.gitignore`:
  ```
  *.sqllite3
  *.pyc
  ```

  Check the status and remote with:
  ```bash
  git status
  git remote -v
  ```

**3. Image Hosting with Cloudinary (Optional):**

- Install packages:
  ```bash
  pip3 install cloudinary django-cloudinary-storage
  ```

  *If not needed, you can uninstall them with:*
  ```bash
  pip3 uninstall cloudinary django-cloudinary-storage
  ```

**4. Database Configuration:**

- Install additional packages:
  ```bash
  pip3 install dj_database_url
  ```

  *Note: Remember to freeze your updated requirements.*
  ```bash
  pip3 freeze > requirements.txt
  ```

- Make database migrations:
  ```bash
  python3 manage.py makemigrations --dry-run
  python3 manage.py migrate --plan
  python3 manage.py migrate
  ```

- Create super user:
  ```bash
  python3 manage.py createsuperuser
  ```

**5. Authentication with Allauth:**

- Install the package:
  ```bash
  pip3 install django-allauth==0.54.0
  ```

  Add configurations to `settings.py`:
  ```python
  # Add this to your INSTALLED_APPS:
  'django.contrib.sites',
  'allauth',
  'allauth.account',
  'allauth.socialaccount',

  # Add these settings:
    SITE_ID = 1  # for social media callback

    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
    ACCOUNT_EMAIL_REQUIRED = True
    ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
    ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE = True
    ACCOUNT_USERNAME_MIN_LENGTH = 4
    LOGIN_URL = '/account/login/'
    LOGIN_REDIRECT_URL = '/'
  
  ```

  Create templates:
  ```bash
  mkdir templates
  mkdir templates/allauth
  cp -r ../.pip-modules/lib/python3.8/site-packages/allauth/templates/* ./templates/allauth/ 
  ```

**6. Static and Media Configuration:**

  ```bash
  mkdir static media static/css
  ```

  Update `settings.py` with:
  ```python
  STATIC_URL = '/static/'
  STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
  MEDIA_URL = '/media/'
  MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
  ```

**7. Deploying with Heroku:**

- Install Heroku CLI:
  ```bash
  curl https://cli-assets.heroku.com/install.sh | sh
  ```

- Login and create app:
  ```bash
  heroku login -i
  heroku create plexosoft
  ```

- Setup environment:
  ```bash
  touch env.py
  ```

  Add the following in `env.py`:
  ```python
  os.environ["DATABASE_URL"] = "<copiedURL>"
  os.environ["SECRET_KEY"]="my_super^secret@key"
  os.environ["IN_DEVELOPMENT"] = "True"
  ```

  Update `settings.py` with provided configurations.

- Set up Heroku variables:
  ```bash
  heroku config:set DISABLE_COLLECTSTATIC=1
  ```

- Create a `Procfile`:
  ```bash
  echo "web: gunicorn django_plexosoft.wsgi:application" > Procfile
  ```

- Finally, deploy to Heroku!

## Simplified Version

1. `pip3 install 'django<4' gunicorn psycopg2`

2. `pip3 freeze > requirements.txt`

3. `django-admin startproject djangopost .`

4. `python3 manage.py startapp blog`  
   (Add to `settings.py` under `INSTALLED_APPS`)

5. `touch .gitignore`  
   Add:  
   ```
   *.sqllite3
   *.pyc
   ```

6. Optional: `pip3 install cloudinary`

7. Optional: `pip3 install django-cloudinary-storage`

8. Optional: 
   ```
   pip3 uninstall cloudinary
   pip3 uninstall django-cloudinary-storage
   ```

9. `pip3 install dj_database_url`

10. `pip3 freeze > requirements.txt`

11. `python3 manage.py makemigrations --dry-run`

12. `python3 manage.py migrate --plan`

13. `python3 manage.py migrate`

14. `python3 manage.py createsuperuser`

15. `git status`

16. `git remote -v`

17. Check Django version: `pip show django | grep Version OR ls ../.pip-modules/lib`

18. `pip3 install django-allauth==0.54.0`  
   (Add the provided settings to `settings.py`)

19. `mkdir templates`

20. `mkdir templates/allauth`

21. `cp -r ../.pip-modules/lib/python3.8/site-packages/allauth/templates/* ./templates/allauth/`

22. `mkdir static`

23. `mkdir media`

24. `mkdir static/css`  
   (Update `settings.py` with provided settings)

25. `curl https://cli-assets.heroku.com/install.sh | sh`

26. `heroku login -i`

27. `heroku create plexosoft`

28. Create a database on ElephantSQL.

29. Create `env.py` and add the given environment variables. Update `settings.py` with the provided configurations.

30. Set up Heroku with the required environment variables.

31. `heroku config:set DISABLE_COLLECTSTATIC=1`

32. Add `HEROKU_HOSTNAME` to Heroku's config vars.

33. Create a `Procfile` for Heroku:
    ```
    echo "web: gunicorn django_plexosoft.wsgi:application" > Procfile
    ```

34. Deploy your project to Heroku.