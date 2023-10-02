import secrets
import string
import random


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
