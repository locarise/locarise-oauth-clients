Locarise OAuth clients
======================

**A collection of OAuth clients for accounts.locarise.com**

---

django-allauth Client
---------------------

Found in the `allauth` folder, this module define a OAuth Locarise provider for
[django-allauth].

### Installation

First you will need to install django-allauth:

    pip install django-allauth

Then edit the following files of your Django project:

`settings.py`:

    TEMPLATE_CONTEXT_PROCESSORS = (
    ...
    "django.core.context_processors.request",
    ...
    "allauth.account.context_processors.account",
    "allauth.socialaccount.context_processors.socialaccount",
    ...
    )

    AUTHENTICATION_BACKENDS = (
    ...
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",

    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
    ...
    )

    INSTALLED_APPS = (
    ...
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # ... include the Locarise providers:
    'locarise_oauth_clients.allauth.providers.locarise',
    )

`urls.py`:

    urlpatterns = patterns('',
    ...
    (r'^accounts/', include('allauth.urls')),
    ...
    )

Go to https://accounts.locarise.com/admin and obtain your `client_id` and
`client_secret` by creating a new *Client* in the admin interface. The callback
uri is `<my-site>/accounts/locarise/login/callback/`.


django-social-auth Client
-------------------------

`settings.py`:

Add [django-social-auth] to your `INSTALLED_APPS`:

    INSTALLED_APPS = (
    ...
    'social_auth'
    )

Add `social_auth` context processor:

    TEMPLATE_CONTEXT_PROCESSORS = (
     ..
     "social_auth.context_processors.social_auth_by_type_backends"
     ...
     )

Add Locarise OAuth2 backend to your `AUTHENTICATION_BACKENDS`:

    AUTHENTICATION_BACKENDS = (
    'locarise_oauth_clients.social_auth.backends.locarise.LocariseOAuth2Backend',
    ...
    'django.contrib.auth.backends.ModelBackend',
    )

Setup required `client_secret` and `client_id` obtained from
https://accounts.locarise.com/admin admin interface. The callback uri is
`<my-site>/complete/locarise-oauth2/`.

    LOCARISE_OAUTH2_CLIENT_ID      = ''
    LOCARISE_OAUTH2_CLIENT_SECRET  = ''

`urls.py`:

    urlpatterns = patterns('',
    ...
    url(r'', include('social_auth.urls')),
    ...
    )

For more information, refer to
[django-social-auth documentation](http://django-social-auth.readthedocs.org/)



[django-allauth]: https://django-allauth.readthedocs.org/en/latest/
[django-social-auth]: https://github.com/omab/django-social-auth
