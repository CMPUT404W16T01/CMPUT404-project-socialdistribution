from django.conf.urls import url, include, patterns
from . import views
from api import views as apiviews
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'posts', apiviews.public_posts)

urlpatterns = [
	url(r'^$', views.feed, name='feed'),
	url(r'^create_post/$', views.create_post, name='create_post'),
	url(r'^logout/$', views.logout, name='logout'),
	url(r'^delete/$', views.delete, name='delete'),
    url(r'^api', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
