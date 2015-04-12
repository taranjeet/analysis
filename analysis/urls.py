from django.conf.urls import patterns, include, url
from django.contrib import admin
from codechef import views
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'analysis.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$','codechef.views.index',name='index'),
    url(r'^analysis/$','codechef.views.analysis',name='analysis'),
)
