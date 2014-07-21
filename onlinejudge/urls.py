from django.conf.urls import patterns, include, url
from django.contrib import admin

from mainapp.views import *
from django.http import HttpResponseRedirect

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'onlinejudge.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', lambda r : HttpResponseRedirect('index')),
    url(r'^index', index),
    url(r'^login', login),
    url(r'^logout', logout),
    url(r'^home', home),
    url(r'^submitprogram', submit_program),
    url(r'^signup', signup),
    url(r'^leaders',leaders),
    url(r'^profile',profile),
    url(r'^allproblems',allproblems),
    url(r'^problem',problem),
    #url(r'^uploadsubmission', upload_submission),
    
    url(r'^admin/', include(admin.site.urls)),
)


urlpatterns += staticfiles_urlpatterns()