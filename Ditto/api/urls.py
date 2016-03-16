from django.conf.urls import url, include, patterns
from . import views
from api import views as api_views
from rest_framework import routers

urlpatterns = [
    url(r'^posts/(?P<pk>[0-9a-z-]+)/comments/$', api_views.post_comments.as_view()),
    url(r'^posts/(?P<pk>[0-9a-z-]+)/$', api_views.post_detail.as_view()),
    url(r'^posts/', api_views.public_posts.as_view()),
    url(r'^author/(?P<pk>[0-9a-z-]+)/posts/$', api_views.author_posts.as_view()),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
    

