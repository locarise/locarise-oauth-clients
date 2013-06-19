from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns
from .provider import LocariseProvider

urlpatterns = default_urlpatterns(LocariseProvider)
