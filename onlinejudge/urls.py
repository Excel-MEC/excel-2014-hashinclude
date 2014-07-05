from django.conf.urls import patterns, include, url
from django.contrib import admin

from mainapp.views import *
from django.http import HttpResponseRedirect

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'onlinejudge.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', lambda r : HttpResponseRedirect('index')),
    url(r'^index', index),
    
    url(r'^admin/', include(admin.site.urls)),
)
