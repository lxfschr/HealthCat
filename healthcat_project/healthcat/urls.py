from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'grumblr.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'healthcat.views.home', name='home'),
    url(r'^profile$', 'healthcat.views.home', name='profile'),
    url(r'^failed-to-connect$', 'healthcat.views.failed_to_connect', name='failed_to_connect'),
    # Route for built-in authentication with our own custom login page
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name':'healthcat/login.html'}, name='login'),
    # Route to logout a user and send them back to the login page
    url(r'^logout$', 'django.contrib.auth.views.logout_then_login', name='logout'),
    url(r'^register$', 'healthcat.views.register', name='register'),
    url(r'^reset_password$', 'healthcat.views.reset_password', name='reset_password'),
    url(r'^change_password$', 'healthcat.views.change_password', name='change_password'),
    url(r'^confirm_registration/(?P<username>[a-zA-Z0-9_@\+\-.]+)/(?P<token>[a-z0-9\-]+)$', 'healthcat.views.confirm_registration', name='confirm_registration'),
    url(r'^confirm_password_reset/(?P<username>[a-zA-Z0-9_@\+\-.]+)/(?P<token>[a-z0-9\-]+)$', 'healthcat.views.confirm_password_reset', name='confirm_password_reset'),
    url(r'^get_owner_photo/(?P<user_id>\d+)$', 'healthcat.views.get_owner_photo', name='get_owner_photo'),
    url(r'^get_pet_photo/(?P<pet_id>\d+)$', 'healthcat.views.get_pet_photo', name='get_pet_photo'),
    url(r'^statistics', 'healthcat.views.statistics', name='statistics'),
    url(r'^notifications', 'healthcat.views.notifications', name='notifications'),
    url(r'^edit-profile$', 'healthcat.views.edit_profile', name='edit_profile'),
    url(r'^add-bowl$', 'healthcat.views.add_bowl', name='add_bowl'),
    url(r'^edit-bowl$', 'healthcat.views.edit_bowl', name='edit_bowl'),
    url(r'^new-rfid-detected/(?P<bowlSerial>[a-zA-Z0-9]+)/(?P<rfid>\d+)$', 
        'healthcat.views.registerRfid'),
    url(r'^add-pet$', 'healthcat.views.add_pet', name='add_pet'),
    url(r'^edit-pet$', 'healthcat.views.edit_pet', name='edit_pet'),
    url(r'^add-feeding-interval$', 'healthcat.views.add_feeding_interval', name='add_feeding_interval'),
    url(r'^get-feeding-intervals/(?P<rfid>\d+)$',
        'healthcat.views.retrieveFeedingIntervals',
            name='get_feeding_intervals'),
    url(r'^edit-feeding-interval$', 'healthcat.views.edit_feeding_interval', name='edit_feeding_interval'),
    url(r'^delete-feeding-interval$', 'healthcat.views.delete_feeding_interval', name='delete_feeding_interval'),
    url(r'^validate-bowl','healthcat.views.validateBowl',name='validate_bowl'),

    #url(r'^notify-bully','healthcat.views.add_bully', name='add_bully'),

    url(r'^is-bowl-connected/','healthcat.views.isBowlConnected',
                name='is_bowl_connected'),
    url(r'^total-consumption','healthcat.views.total_consumption',
                name='total_consumption'),
    url(r'^consumption-over-time','healthcat.views.consumption_over_time',
                name='consumption_over_time'),
    url(r'^total-bullying-instances','healthcat.views.total_bullying_instances',
                name='total_bullying_instances'),
    url(r'^total-bullied-instances','healthcat.views.total_bullied_instances',
                name='total_bullied_instances'),

)
