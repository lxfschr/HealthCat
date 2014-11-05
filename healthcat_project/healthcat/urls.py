from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'grumblr.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'healthcat.views.home'),
    # Route for built-in authentication with our own custom login page
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name':'healthcat/login.html'}, name='login'),
    # Route to logout a user and send them back to the login page
    url(r'^logout$', 'django.contrib.auth.views.logout_then_login'),
    url(r'^register$', 'healthcat.views.register', name='register'),
    url(r'^reset_password$', 'healthcat.views.reset_password', name='reset_password'),
    url(r'^change_password$', 'healthcat.views.change_password', name='change_password'),
    url(r'^confirm-registration/(?P<username>[a-zA-Z0-9_@\+\-.]+)/(?P<token>[a-z0-9\-]+)$', 'healthcat.views.confirm_registration', name='confirm_registration'),
    url(r'^confirm-password-reset/(?P<username>[a-zA-Z0-9_@\+\-.]+)/(?P<token>[a-z0-9\-]+)$', 'healthcat.views.confirm_password_reset', name='confirm_password_reset'),
)
