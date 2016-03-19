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

    # Friend API
    url(r'^friends/(?P<pk1>[0-9a-z-]+)/(?P<pk2>[0-9a-z-]+)', views.check_mutual_friend.as_view()),
    url(r'^friendrequest/$', views.friend_request.as_view(), name='friendrequest'),


    # API Auth
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
 