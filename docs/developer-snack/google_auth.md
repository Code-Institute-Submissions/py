## Google OAuth Integration Guide

This comprehensive guide aims to facilitate the integration of Google OAuth 2.0 with a Django application using the Django Allauth package. Below are the official documentation sources you may find useful for a more in-depth understanding:

1. **Google OAuth 2.0 Official Documentation**: [Google OAuth 2.0](https://developers.google.com/identity/protocols/oauth2) | [Setting Up OAuth 2.0](https://support.google.com/cloud/answer/6158849?hl=en)
2. **Django Allauth Documentation**: [Allauth Official Guide](https://django-allauth.readthedocs.io/en/latest/index.html)
3. **Django Authentication Documentation**: [Django Auth Official Docs](https://docs.djangoproject.com/en/3.2/topics/auth/)

---

### STEP 0: Initial Setup

#### Google Cloud Platform Console
1. Navigate to the [Google Cloud Platform Console](https://console.cloud.google.com/).
2. Choose an existing project or create a new one from the projects list.

#### Django `settings.py` Configuration
1. Add the Google Allauth application to your `INSTALLED_APPS` list in `settings.py`:
    ```python
    INSTALLED_APPS = [
        'allauth.socialaccount.providers.google',
        # ... other installed apps
    ]
    ```

2. Set environment variables for Google Client ID and Secret:
    ```python
    import os
    # ... other imports

    os.environ['GOOGLE_CLIENT_ID'] = "placeholder_client_id"
    os.environ['GOOGLE_SECRET'] = "placeholder_secret_key"
    # ... remaining settings
    ```

---

### STEP 1: OAuth Client Configuration

#### Navigational Steps
1. Head over to the [OAuth Consent Screen](https://console.cloud.google.com/apis/credentials/consent).
2. If not already opened, expand the console’s left-side menu and select **APIs & Services**.
3. Continue to the [Credentials Page](https://console.developers.google.com/apis/credentials).

#### Create OAuth Client
1. Click **Create credentials** and select **OAuth client ID**.
2. Choose **Web application** as the application type.

#### Authorized Domains & Redirect URIs
1. **Authorized JavaScript Origins**: Define the domains from which OAuth 2.0 requests can be made.
    - Development: `http://localhost:8000`
    - Production: `https://www.example.com`
  
2. **Authorized Redirect URIs**: Specify the URIs to which the user will be redirected post-login.
    - Development: `http://localhost:8000/accounts/google/login/callback/`
    - Production: `https://www.example.com/accounts/google/login/callback/`

    **Note**: Include both development and production URLs if you're using multiple environments. Make sure to adapt these paths to align with your specific Django URL routing and third-party app configurations.

---

### STEP 2: Django Configuration

#### Update `settings.py`

Add the following configurations to your Django `settings.py` file:

```python
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': os.environ.get('GOOGLE_CLIENT_ID'),
            'secret': os.environ.get('GOOGLE_SECRET'),
            'key': ''
        }
    }
}
```

#### STEP 2.1: Site Configuration

1. **Via Django Admin Panel or Shell**: To configure site settings, run the following commands in the Django shell:
    ```python
    python3 manage.py shell
    from django.contrib.sites.models import Site

    # Development:
    dev_site = Site.objects.create(domain='dev.example.com', name='Development Site')

    # Production:
    prod_site = Site.objects.create(domain='www.example.com', name='Production Site')

    print(f"Development Site ID: {dev_site.id}")
    print(f"Production Site ID: {prod_site.id}")
    ```

2. **Verify Site IDs**: To view all configured sites, execute the following code snippet:
    ```python
    from django.contrib.sites.models import Site
    all_sites = Site.objects.all()

    for site in all_sites:
        print(f"ID: {site.id}, Domain: {site.domain}, Name: {site.name}")
    ```

#### STEP 2.2: Add `SITE_ID` to `settings.py`

Depending on your environment (development or production), update the `SITE_ID` accordingly:

```python
if IN_DEVELOPMENT:
    SITE_ID = 1  # Development domain ID
else:
    SITE_ID = 2  # Production domain ID
```

---

### STEP 3: Debugging Common Issues

#### Error 400: `redirect_uri_mismatch`
If you encounter an Error 400, scrutinize the error message from Google Auth. Update the 'Authorized Redirect URIs' and 'Authorized JavaScript Origins' in the Google Cloud Console to match the URI provided in the error message. For example, you might need to add a Heroku-specific domain like `https://your-app-name.herokuapp.com`.

By following these steps meticulously, you should be well on your way to integrating Google OAuth 2.0 into your Django application.

### STEP 4: Login Button

We have created the following Google Login button:

- [Logo Images](https://developers.google.com/identity/branding-guidelines)

=== "HTML"

    ``` html
    ...
    {% get_providers as socialaccount_providers %}
        {% if socialaccount_providers %}

        <!-- Google Login Button -->
        <a href="{% provider_login_url 'google' method='oauth2' %}" class="btn google-button">
            <span class="google-icon"></span>
            <span class="btn-text text-center">Sign in with Google</span>
        </a>

        {% include "socialaccount/snippets/login_extra.html" %}
        {% endif %}
    ...
    ```

=== "CSS"

    ``` css
    /* Google Button Login */
    .google-button {
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: #4285F4;
        color: white;
        border-radius: 5px 5px 0px 0px;
        /* box-shadow: 0 3px 4px 0 rgba(0, 0, 0, 0.25); */
        font-family: 'Roboto', sans-serif;
        font-weight: 500;
        font-size: 14px;
        display: flex;
        align-items: center;
    }

    .google-icon {
        background: url('/static/frontend/assets/btn_google_light_normal_ios.svg') transparent 5px 50% no-repeat;
        display: inline-block;
        vertical-align: middle;
        width: 60px;
        height: 42px;
    }

    .btn-text {
        font-size: 14px;
        font-weight: 500;
    }
    ```
