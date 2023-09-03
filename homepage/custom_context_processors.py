# custom_context_processors.py

from allauth.account.models import EmailAddress


def get_verified_email(request):
    try:
        email_object = EmailAddress.objects.get(user=request.user)
        if email_object.verified:
            return {'get_verified_email': email_object.email}
    except EmailAddress.DoesNotExist:
        pass
    return {'get_verified_email': None}
