# Global context processor for EmailAddress model

from allauth.account.models import EmailAddress


def get_verified_email(request):
    if request.user.is_authenticated:
        try:
            email_object = EmailAddress.objects.get(user=request.user)
            if email_object.verified:
                return {'get_verified_email': email_object}
        except EmailAddress.DoesNotExist:
            pass
    return {'get_verified_email': None}
