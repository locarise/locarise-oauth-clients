"""
Locarise OAuth 2.0 support
"""
import os
import json

from urllib2 import Request

from django.contrib.auth import get_user_model
from social_auth.backends import OAuthBackend, BaseOAuth2
from social_auth.utils import dsa_urlopen


# Locarise OAuth2 base configuration
LOCARISE_OAUTH2_SERVER = os.environ.get('LOCARISE_OAUTH2_SERVER', 'accounts.locarise.com')
LOCARISE_OAUTH2_TOKEN_URL = os.environ.get('LOCARISE_OAUTH2_TOKEN_URL', 'https://accounts.locarise.com/oauth2/access_token')
LOCARISE_OAUTH2_AUTHORIZATION_URL = os.environ.get('LOCARISE_OAUTH2_AUTHORIZATION_URL', 'https://accounts.locarise.com/oauth2/authorize')

# scope for user email, specify extra scopes in settings, for example:
LOCARISE_OAUTH2_SCOPE = ['read']
LOCARISE_API_PROFILE = os.environ.get('LOCARISE_API_PROFILE', 'https://accounts.locarise.com/userinfo.json')


User = get_user_model()


# Backends
class LocariseOAuth2Backend(OAuthBackend):

    """Locarise OAuth authentication backend"""
    name = 'locarise-oauth2'

    EXTRA_DATA = [
        ('refresh_token', 'refresh_token', True),
        ('expires_in', 'expires'),
        ('token_type', 'token_type', True)
    ]
    ID_KEY = 'uid'

    def get_user_details(self, response):
        email = response.get('email', '')
        return {'username': email.split('@', 1)[0],
                'email': email,
                'fullname': response.get('first_name', '') + ' ' + response.get('last_name', ''),
                'first_name': response.get('first_name', ''),
                'last_name': response.get('last_name', ''),
                'is_staff': response.get('is_staff', ''),
                'locale': response.get('locale', ''),
                'uid': response.get('uid', '')}


class LocariseOAuth2(BaseOAuth2):

    """Locarise OAuth2 support"""
    AUTH_BACKEND = LocariseOAuth2Backend
    AUTHORIZATION_URL = LOCARISE_OAUTH2_AUTHORIZATION_URL
    ACCESS_TOKEN_URL = LOCARISE_OAUTH2_TOKEN_URL
    SETTINGS_KEY_NAME = 'LOCARISE_OAUTH2_CLIENT_ID'
    SETTINGS_SECRET_NAME = 'LOCARISE_OAUTH2_CLIENT_SECRET'
    SCOPE_VAR_NAME = 'LOCARISE_OAUTH_EXTRA_SCOPE'
    DEFAULT_SCOPE = LOCARISE_OAUTH2_SCOPE
    REDIRECT_STATE = False

    def user_data(self, access_token, *args, **kwargs):
        """Return user data from Locarise API"""
        return locariseapis_profile(LOCARISE_API_PROFILE, access_token)


def locariseapis_profile(url, access_token):
    """
    Loads user data from Locarise Sane Account Managemt Service, such as name,
    first_name, last_name, etc. as it's described in:
    https://accounts.locarise.com/userinfo
    """
    # WARNING: This doesn't verify the certificate, should use requests instead
    request = Request(url)
    request.add_unredirected_header(
        'Authorization', 'Bearer %s' % access_token)
    try:
        return json.loads(dsa_urlopen(request).read())
    except (ValueError, KeyError, IOError):
        return None


def associate_user_by_uid(backend, user, uid, social_user=None, *args, **kwargs):
    if user:
        return {'user': user, 'social_user': social_user, 'new_association': False}

    # e-mail has to be set straight away at creation to avoid breaking the
    # 'unique' condition when multiple accounts are pending.
    user, created = User.objects.get_or_create(uid=uid, defaults=dict(email=kwargs['details']['email']))
    return {'user': user, 'social_user': social_user, 'new_association': created}


# Backend definition
BACKENDS = {
    'locarise-oauth2': LocariseOAuth2,
}
