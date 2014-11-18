from django.conf.urls import patterns, include, url		
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from vidavid import views

urlpatterns = patterns('',
    url(r'^$', views.login_user),
    url(r'^login$', views.login_user, name = 'login'),
    url(r'^logout$', views.logout_user, name = 'logout'),
    url(r'^auth$', views.auth, name = 'auth'),
    url(r'^register$', views.register, name = 'register'),
    url(r'^index$', views.index, name = 'index'),
    url(r'^profile/(?P<id>\d+)$', views.profile, name='profile'),
    url(r'^post-video$', views.post_video, name='post-video'),
)

urlpatterns += staticfiles_urlpatterns()