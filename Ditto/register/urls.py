from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.register, name='register'),
	url(r'^sign_up/$', views.sign_up, name='sign_up'),
	url(r'^confirm/$', views.confirm, name='confirm'),
	url(r'^fail/$', views.fail, name='fail'),
]

