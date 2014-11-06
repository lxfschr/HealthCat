from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'kcProject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^openornot/(?P<catID>\d+)/(?P<timeNow>\d\d\d\d)/(?P<YYYYMMDD>\d\d\d\d\d\d\d\d)$','bowlApp.views.openornot'),
    url(r'^rfidtopetid/(?P<rfid>\d+)$','bowlApp.views.rfidtopetid'),
    url(r'^', include('bowlApp.urls')),

)
