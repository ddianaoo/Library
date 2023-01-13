from .models import CustomUser
from django import forms

from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
import base64


class EmailAuthBackend(object):
    """
    Authenticate using e-mail account.
    """

    def authenticate(self, email=None, password=None, role=None):
        user = CustomUser.get_by_email(email=email)
        if user is None:
            raise forms.ValidationError('Неккоректний адрес електронної пошти')
        if role is not None:
            if str(user.role) != str(role):
                raise forms.ValidationError('Неккоректна роль для цього аккаунту')
        if not user.check_password(password):
            raise forms.ValidationError('Неккоректний пароль')
        return user

    def get_user(self, user_id):
        return CustomUser.get_by_id(user_id)


def get_authorization_header(request):
    auth = request.META.get("HTTP_AUTHORIZATION", "")
    return auth


class BasicAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != "basic":
            return None

        if len(auth) == 1:
            raise exceptions.AuthenticationFailed("Invalid basic header. No credentials provided.")
        if len(auth) > 2:
            raise exceptions.AuthenticationFailed("Invalid basic header. Credential string is not properly formatted")
        try:
            auth_decoded = base64.b64decode(auth[1]).decode("utf-8")
            #print(auth_decoded)
            email, password = auth_decoded.split(":")
        except (UnicodeDecodeError, ValueError):
            raise exceptions.AuthenticationFailed("Invalid basic header. Credentials not correctly encoded")

        return self.authenticate_credentials(email, password, request)

    def authenticate_credentials(self, email, password, request=None):
        credentials = {
            'email': email,
            "password": password
        }

        user = EmailAuthBackend().authenticate(**credentials)

        if user is None:
            raise exceptions.AuthenticationFailed("Invalid email or password")

        # if not user.is_active:
        #     raise exceptions.AuthenticationFailed("User is inactive")

        return user, None