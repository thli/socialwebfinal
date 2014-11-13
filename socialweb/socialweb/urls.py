from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^vidavid/', include('vidavid.urls')),
    url(r'^$', include('vidavid.urls')),
)
