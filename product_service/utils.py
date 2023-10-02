import secrets
import string
import random
import os
from django.core.cache import cache
from datetime import datetime, timedelta
from functools import wraps
from django.http import HttpResponse, HttpResponseForbidden


def generate_download_token(length=12):
    """
    Generate a download token of the specified length.
    """
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))


def generate_random_password(length=12):
    """
    Generate a random password of the specified length.
    """
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password


def custom_upload_to(instance, filename):
    """
    Generates a unique filename based on the instance's token.
    For the Download model.
    """
    ext = filename.split('.')[-1]
    return os.path.join('downloads', f'{instance.token}.{ext}')


def check_rate_limit(request):
    """
    Checks if the rate limit for the given request has been exceeded.

    Parameters:
    - request: HttpRequest object

    Returns:
    - HttpResponse with a 429 status code if the rate limit is exceeded.
    - HttpResponse with a 403 status code if the user is not authenticated.
    - None otherwise.
    The function uses Django's cache framework to keep track of the number
    of requests made by each user (or by anonymous users)
    within a 60-second window. Error if the rate limit (3 requests per minute)
    is exceeded.
    """

    if not request.user.is_authenticated:
        return HttpResponseForbidden("You must be logged in to download files.")

    user_id = str(request.user.id)
    cache_key = f"rate_limit_{user_id}"
    rate_limit_info = cache.get(
        cache_key, {'count': 0, 'timestamp': datetime.now()})

    if rate_limit_info['count'] >= 3 and (datetime.now() - rate_limit_info['timestamp']).seconds < 60:
        return HttpResponse('Too many requests', status=429)

    if (datetime.now() - rate_limit_info['timestamp']).seconds >= 60:
        rate_limit_info = {'count': 1, 'timestamp': datetime.now()}
    else:
        rate_limit_info['count'] += 1

    cache.set(cache_key, rate_limit_info, timeout=60)
    return None
