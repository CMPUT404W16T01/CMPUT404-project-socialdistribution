from django.conf.urls import url, patterns
from django.conf import settings
from . import views

urlpatterns = [

	url(r'^$', views.feed, name='feed'),
	url(r'^create_post/$', views.create_post, name='create_post'),
	url(r'^logout/$', views.logout, name='logout'),
	url(r'^delete/$', views.delete, name='delete'),
	url(r'^create_comment/$', views.create_comment, name='create_comment'),
	url(r'^profile/$', views.profile, name='profile'),
	url(r'^author/(?P<pk>[0-9a-z-]+)/?profile/$', views.get_profile, name='get_profile'),

]

#http://stackoverflow.com/questions/5517950/django-media-url-and-media-root
if settings.DEBUG:
     urlpatterns += patterns('',
         (r'^ditto/media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),) 
