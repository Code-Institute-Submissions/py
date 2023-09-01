# Django Imports
from django.shortcuts import redirect
from django.views import View


class UserRoleRedirectView(View):
    '''' Proper redirect based on the user's role '''

    def get(self, request, *args, **kwargs):
        user = request.user

        if user.role == 0:
            return redirect('/account/user/')
        elif user.role == 1:
            return redirect('/account/admin/')
        else:
            return redirect('/account//user/')
