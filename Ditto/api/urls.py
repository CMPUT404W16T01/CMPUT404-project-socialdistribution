from django.conf.urls import url
from snippets import views

urlpatterns = [
    url(r'^posts/$', views.public_posts),
    url(r'^posts/(?P<pk>[0-9a-z-]+)/$', views.post_detail),
]