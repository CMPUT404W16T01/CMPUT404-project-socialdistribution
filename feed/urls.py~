from django.conf.urls import url, include, patterns
from . import views
from api import views as api_views
from rest_framework import routers

urlpatterns = [

    url(r'^$', views.feed, name='feed'),
    url(r'^create_post/$', views.create_post, name='create_post'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^delete/$', views.delete, name='delete'),
    url(r'^create_comment/$', views.create_comment, name='create_comment'),


]
