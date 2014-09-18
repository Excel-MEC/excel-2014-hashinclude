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
    url(r'^fblogin', fblogin),
    url(r'^signup', signup),
    url(r'^signin', index),
    url(r'^leaderboard',leaders),
    url(r'^discussion',discussionboard),
    url(r'^profile',profile),
    url(r'^allproblems',allproblems),
    url(r'^submit',problem),
    url(r'^upload',upload),
    url(r'^fullscreen',fullscreen),
    url(r'^createquestion',createquestion),
    url(r'^contactus',contactus),
    url(r'^rules',rules),
    url(r'^submission',submission),
    #url(r'^uploadsubmission', upload_submission),
    
    url(r'^admin/', include(admin.site.urls)),
)


urlpatterns += staticfiles_urlpatterns()