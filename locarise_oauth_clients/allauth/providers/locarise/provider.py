from allauth.socialaccount import providers
from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider


class LocariseAccount(ProviderAccount):
    def get_profile_url(self):
        return self.account.extra_data.get('link', '')

    def get_avatar_url(self):
        return self.account.extra_data.get('picture', '')

    def to_str(self):
        dflt = super(LocariseAccount, self).to_str()
        return self.account.extra_data.get('email', dflt)


class LocariseProvider(OAuth2Provider):
    id = 'locarise'
    name = 'Locarise'
    package = 'locarise_oauth_clients.allauth.providers.locarise'
    account_class = LocariseAccount
    supports_state = False

providers.registry.register(LocariseProvider)
