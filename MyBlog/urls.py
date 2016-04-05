from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    url(r'^$', 'blog.views.home', name='home'),
    # url(r'^$', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^tag/$', 'blog.views.get_tags', name='get_tags'),
    url(r'^tag/(\S+)/$', 'blog.views.get_list_by_tag', name='get_list_by_tag'),
    url(r'^category/(\S+)/$', 'blog.views.get_list_by_category', name='get_list_by_category'),
    url(r'^about/$', 'blog.views.about_me', name='about-me'),

    url(r'^(\S+)/$', 'blog.views.get_blog_by_url', name='get_blog_by_url'),
]
