from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    url(r'^$', 'blog.views.home', name='home'),
    # url(r'^$', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^(\S+)/$', 'blog.views.get_by_url', name='get_by_url'),
]
