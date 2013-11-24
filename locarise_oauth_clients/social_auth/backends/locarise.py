"""
Locarise OAuth 2.0 support
"""
from urllib2 import Request

from django.utils import simplejson

from social_auth.backends import OAuthBackend, BaseOAuth2
from social_auth.utils import dsa_urlopen


# Locarise OAuth2 base configuration
LOCARISE_OAUTH2_SERVER = 'accounts.locarise.com'
LOCARISE_OATUH2_AUTHORIZATION_URL = 'https://accounts.locarise.com/oauth2/authorize'

# scope for user email, specify extra scopes in settings, for example:
LOCARISE_OAUTH2_SCOPE = ['read']
LOCARISE_API_PROFILE = 'https://accounts.locarise.com/userinfo.json'


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
                'membership_set': response.get('membership_set', ''),
                'uid': response.get('uid', '')}


class LocariseOAuth2(BaseOAuth2):

    """Locarise OAuth2 support"""
    AUTH_BACKEND = LocariseOAuth2Backend
    AUTHORIZATION_URL = 'https://accounts.locarise.com/oauth2/authorize'
    ACCESS_TOKEN_URL = 'https://accounts.locarise.com/oauth2/access_token'
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
        return simplejson.loads(dsa_urlopen(request).read())
    except (ValueError, KeyError, IOError):
        return None


# Backend definition
BACKENDS = {
    'locarise-oauth2': LocariseOAuth2,
}
