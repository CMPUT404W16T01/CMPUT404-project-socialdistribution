from django.conf.urls import url, include, patterns
from . import views
from api import views as api_views
from rest_framework import routers

urlpatterns = [
    url(r'^$', views.feed, name='feed'),
    url(r'^create_post/$', views.create_post, name='create_post'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^delete/$', views.delete, name='delete'),
    url(r'^api/posts/(?P<pk>[0-9a-z-]+)/$', api_views.post_detail.as_view()),
    url(r'^api/posts/', api_views.public_posts.as_view()),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
