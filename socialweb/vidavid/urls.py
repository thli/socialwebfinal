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
    url(r'^profile/edit$', views.edit_profile, name='edit'),
    url(r'^profile/(?P<id>\d+)$', views.profile, name='profile'),
    url(r'^post-video$', views.post_video, name='post-video'),
    url(r'^update-index$', views.update_index, name = 'update-index'),
    url(r'^like-post$', views.like_post, name = 'like-post'),
    url(r'^change-password$', views.update_password, name = 'change-password'),
    url(r'^search$', views.search, name = 'search'),
    url(r'^img/(?P<id>\d+)$', views.get_profile_photo, name = 'profile-pic'),
)

urlpatterns += staticfiles_urlpatterns()