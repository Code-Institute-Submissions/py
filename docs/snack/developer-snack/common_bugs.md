## Common Bug Solution

### 1. Collectstatic Issues: During Heroku Deployment

When deploying a Django application on Heroku, you may encounter an error that looks like this:

```bash
django.core.exceptions.ImproperlyConfigured: You're using the staticfiles app without having set the STATIC_ROOT setting to a filesystem path.
```

This error occurs because the `STATIC_ROOT` setting is missing or not properly configured in your Django `settings.py` file.

## Solution

### Step 1: Add `STATIC_ROOT` to `settings.py`

Open your `settings.py` file and locate the section that deals with static files, usually toward the bottom of the file. If `STATIC_ROOT` is not present, add it like so:

```python
# settings.py

# ... (other settings)

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

# Where your static files exist locally
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

# Add this line to specify where collectstatic will collect static files for deployment
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# ... (other settings)
```

**Explanation:**

- `STATIC_URL`: URL to use when referring to static files located in `STATIC_ROOT`.
- `STATICFILES_DIRS`: This setting defines the location of static files in your local development environment.
- `STATIC_ROOT`: This new setting specifies the directory where `collectstatic` will collect static files for deployment.

### Step 2: Commit the Changes to Git

After you've made this change, save the `settings.py` file and commit the change to your Git repository:

```bash
git add .
git commit -m "Added STATIC_ROOT in settings.py"
```

### Step 3: Deploy to Heroku

Push your changes to Heroku to deploy the application from the website or from the CLI:

```bash
git push heroku main
```

This will automatically run the `collectstatic` command as part of the deployment process, and you should not see the `ImproperlyConfigured` error anymore.

## Conclusion

Adding the `STATIC_ROOT` setting in your `settings.py` file will solve the issue with the `collectstatic` command when deploying your Django application to Heroku. Make sure to commit your changes and redeploy for the issue to be resolved.