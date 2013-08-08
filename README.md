Locarise OAuth clients
======================

**A collection of OAuth clients for accounts.locarise.com**

---

This module implements a OAuth 2.0 clients in several popular Django social
authentication apps. To install this module in your project, install with `pip`
as follow:

    pip install git+https://github.com/Locarise/locarise-oauth-clients.git

And refer to the corresponding social app.


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
        'django.core.context_processors.request',
        ...
        'allauth.account.context_processors.account',
        'allauth.socialaccount.context_processors.socialaccount',
        ...
    )

    AUTHENTICATION_BACKENDS = (
        ...
        # Needed to login by username in Django admin, regardless of `allauth`
        'django.contrib.auth.backends.ModelBackend',

        # `allauth` specific authentication methods, such as login by e-mail
        'allauth.account.auth_backends.AuthenticationBackend',
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

### Installation

`settings.py`:

Add [django-social-auth] to your `INSTALLED_APPS`:

    INSTALLED_APPS = (
        ...
        'social_auth'
    )

Add `social_auth` context processor:

    TEMPLATE_CONTEXT_PROCESSORS = (
         ..
         'social_auth.context_processors.social_auth_by_type_backends'
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


Google Apps Auth for Internal Django Sites
------------------------------------------

Inspired by [this article](http://techblog.safaribooksonline.com/2012/11/02/google-apps-auth-for-internal-django-sites/)

The purpose is to let people login with their google accounts only from
the locarise.com domain which is managed by Google.
The setup is based on [django-social-auth].

### Installation

In your `settings.py`:

    INSTALLED_APPS = (
        ...
        'social_auth'
    )

    AUTHENTICATION_BACKENDS = (
        'social_auth.backends.google.GoogleOAuth2Backend',  # putting this 1st means that most users will auth with their Google identity
        'django.contrib.auth.backends.ModelBackend',        # ...but this one means we can still have local admin accounts as a fallback
    )

    LOGIN_URL          = '/login/google-oauth2/'
    LOGIN_ERROR_URL    = '/login-error/'

    SOCIAL_AUTH_RAISE_EXCEPTIONS = False
    SOCIAL_AUTH_PROCESS_EXCEPTIONS = 'social_auth.utils.log_exceptions_to_messages'  # ...assuming you like the messages framework

    GOOGLE_OAUTH2_CLIENT_ID      = 'yourCLIENTidHERE'  # this is on the credentials web page from above
    GOOGLE_OAUTH2_CLIENT_SECRET  = 'YOURsecretHERE'    # this is also on the credentials web page from above
    GOOGLE_WHITE_LISTED_DOMAINS = ['locarise.com']  # this is what actually limits access

    SOCIAL_AUTH_COMPLETE_URL_NAME  = 'socialauth_complete'
    SOCIAL_AUTH_ASSOCIATE_URL_NAME = 'socialauth_associate_complete'

In `urls.py`:

    ...
    from django.contrib.auth.decorators import login_required
    from django.contrib.auth.views import logout
    from django.views.generic import TemplateView
    ...

    urlpatterns += patterns('',
        url(r'', include('social_auth.urls')),

        url(r'^$', TemplateView.as_view(template_name='login.html')),
        url(r'^logout/$', logout, {'next_page': '/'}, name='gauth_logout'),

        url(r'^login-error/$', TemplateView.as_view(template_name='login-error.html')),

    )

In the `login.html` template:

    <p>Use your work email credentials to sign in to this application:
      <a href="{% url 'socialauth_begin' 'google-oauth2' %}?next=/">Sign In</a>
    </p>


[django-allauth]: https://django-allauth.readthedocs.org/en/latest/
[django-social-auth]: https://github.com/omab/django-social-auth
