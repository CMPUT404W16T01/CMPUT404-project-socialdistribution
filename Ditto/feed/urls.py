from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.feed, name='feed'),
	url(r'^create_post/$', views.create_post, name='create_post'),
	url(r'^logout/$', views.logout, name='logout'),

]

