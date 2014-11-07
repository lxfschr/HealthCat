from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'kcProject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^openornot/(?P<rfid>\d+)/(?P<timenow>\d\d\d\d)/(?P<YYYYMMDD>\d\d\d\d\d\d\d\d)$','bowlApp.views.openornot'),
    # url(r'^rfidtopetid/(?P<rfid>\d+)$','bowlApp.views.rfidtopetid'), ## depricated
    url(r'^createpet/(?P<rfid>\d+)','bowlApp.views.createPet'),
    url(r'^createschedule/(?P<nameOfSch>[a-zA-Z0-9]+)','bowlApp.views.createSchedule'),
    url(r'^updatescheduleadd/(?P<schID>\d+)/(?P<timein>\d\d\d\d)/(?P<timeout>\d\d\d\d)/(?P<amount>\d+)',
    	'bowlApp.views.updateScheduleAdd'),
    url(r'^updatescheduleremove/(?P<tawID>[a-zA-Z0-9]+)',
    	'bowlApp.views.updateScheduleRemove'),
    url(r'^createpet/(?P<rfid>\d+)','bowlApp.views.createPet'),
    url(r'^connect','bowlApp.views.connect'),


)
