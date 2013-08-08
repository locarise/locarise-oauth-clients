import requests

from allauth.socialaccount.providers.oauth2.views import (OAuth2Adapter,
                                                          OAuth2LoginView,
                                                          OAuth2CallbackView)

from allauth.socialaccount.models import SocialLogin, SocialAccount
from allauth.socialaccount.adapter import get_adapter

from .provider import LocariseProvider


class LocariseOAuth2Adapter(OAuth2Adapter):
    provider_id = LocariseProvider.id
    access_token_url = 'https://accounts.locarise.com/oauth2/access_token'
    authorize_url = 'http://accounts.locarise.com/oauth2/authorize'
    profile_url = 'http://accounts.locarise.com/userinfo.json'

    def complete_login(self, request, app, token, **kwargs):
        resp = requests.get(self.profile_url,
                            headers={'Authorization': 'Bearer ' + token.token})
        extra_data = resp.json()
        uid = str(extra_data['uid'])
        user = get_adapter() \
            .populate_new_user(email=extra_data.get('email'),
                               last_name=extra_data.get('last_name'),
                               first_name=extra_data.get('first_name'))
        account = SocialAccount(user=user,
                                uid=uid,
                                provider=self.provider_id,
                                extra_data=extra_data)
        return SocialLogin(account)

oauth2_login = OAuth2LoginView.adapter_view(LocariseOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(LocariseOAuth2Adapter)
