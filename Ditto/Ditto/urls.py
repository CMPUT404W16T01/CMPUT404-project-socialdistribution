from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'Ditto.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^register/', include('register.urls', namespace='register')),
    url(r'^admin/', include(admin.site.urls)),

]
