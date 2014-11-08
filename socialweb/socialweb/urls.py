from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^vinterest/', include('vinterest.urls')),
    url(r'^$', 'vinterest.views.index'),
)
