"""ditto URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from api import views as api_views

urlpatterns = [
    # Examples:
    # url(r'^$', 'Ditto.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^register/', include('register.urls', namespace='register')),
    url(r'^confirm/', include('register.urls', namespace='confirm')),
    url(r'^login/', include('login.urls', namespace='login')),
    url(r'^feed/', include('feed.urls', namespace='feed')),
    url(r'^settings/', include('settings.urls', namespace='settings')),
    url(r'^friends/', include('friends.urls', namespace='friends')),
    url(r'^', include('feed.urls')),
    url(r'^api/posts/(?P<pk>[0-9a-z-]+)/comments/$', api_views.PostComments.as_view()),
    url(r'^api/posts/(?P<pk>[0-9a-z-]+)/$', api_views.PostDetail.as_view()),
    url(r'^api/posts/', api_views.PublicPosts.as_view()),
    url(r'^api/author/(?P<pk>[0-9a-z-]+)/posts/$', api_views.AuthorPosts.as_view()),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
