from django.conf.urls import url, include, patterns
from . import views
from rest_framework import routers

urlpatterns = [
	# Posts API

    url(r'^posts/(?P<pk>[0-9a-z-]+)/comments/$',    views.post_comments.as_view()),
	url(r'^posts/(?P<pk>[0-9a-z-]+)/$',             views.post_detail.as_view()),
    url(r'^posts/', 								views.public_posts.as_view()),


    # Author API
    url(r'^author/(?P<pk>[0-9a-z-]+)/$', 			views.author_detail.as_view()),
    url(r'^author/(?P<pk>[0-9a-z-]+)/posts/$', 		views.author_posts.as_view()),
    url(r'^author/(?P<pk>[0-9a-z-]+)/comments/$', 	views.author_comments.as_view()),

    # API Auth
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
 