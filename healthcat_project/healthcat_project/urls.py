from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'healthcat_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^healthcat/', include('healthcat.urls')),
    url(r'^$', 'healthcat.views.home', name='home'),
)
