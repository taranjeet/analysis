from django.conf.urls import patterns, include, url
from django.contrib import admin
from codechef import views
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'analysis.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^analysis/$','codechef.views.analysis',name='analysis'),
    # url(r'^details/','codechef.views.updateProblems',name='updateProblems'),
    url(r'^check','codechef.views.userDetails',name='userDetails'),
    url(r'^friends','codechef.views.addFriends',name='addFriends'),
    url(r'^getChapterList','codechef.views.getChapterList',name='getChapterList'),
)
