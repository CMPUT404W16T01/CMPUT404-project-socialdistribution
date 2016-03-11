from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^$', views.feed, name='feed'),
    url(r'^create_post/$', views.create_post, name='create_post'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^delete/$', views.delete, name='delete'),
    url(r'^create_comment/$', views.create_comment, name='create_comment'),


]
