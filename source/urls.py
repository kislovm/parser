from django.conf.urls import patterns, include, url

import lingvo.views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'source.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^parse/$', 'lingvo.views.main', name='main'),
    url(r'^dictionaries/$', 'lingvo.views.dictionaries', name='dictionaries'),
    url(r'^dictionary/(?P<id>\d+)/$', 'lingvo.views.dictionary', name='dictionary'),
)
