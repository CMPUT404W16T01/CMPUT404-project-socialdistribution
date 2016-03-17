from django.conf.urls import include, url
from django.contrib import admin

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
    url(r'^api/', include('api.urls', namespace='api')),
    url(r'^', include('feed.urls')),
]
