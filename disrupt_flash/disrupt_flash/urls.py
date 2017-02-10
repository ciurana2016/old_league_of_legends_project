from django.conf.urls import include, url
from django.contrib import admin

from content.views import *
from blog.views import BlogPostsView, BlogPostView



urlpatterns = [
    
    # Main webpage
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^contact/$', ContactView.as_view(), name='contact'),
    url(r'^start/$', StartView.as_view()),
    url(r'^r/(?P<slug>[_\w]+)/$', RoomView.as_view()),
    url(r'^welcome_to_te_league_of_draven/$', BuildTeamView.as_view()),
    url(r'^close_room/$', CloseRoomView.as_view(), name='close_room'),

    # Blog
    url(r'^blog/$', BlogPostsView.as_view(), name='blog_posts'),
    url(r'^blog/(?P<slug>[_\w]+)/$', BlogPostView.as_view(), name='blog_post'),

    # TTTT
    url(r'^supporters/$', SupportersView.as_view(), name='supporters'),


    url(r'^admin/', include(admin.site.urls)),
]
