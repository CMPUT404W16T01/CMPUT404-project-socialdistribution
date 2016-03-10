from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.settings, name='settings'),
	url(r'^save_settings', views.save_settings, name="save_settings"),
]
