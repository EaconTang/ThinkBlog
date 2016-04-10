from django.conf.urls import include, url, handler404, handler500
from django.contrib import admin
from rest_framework import routers
from blog import views as blog_views

router = routers.DefaultRouter()
router.register(r'mdfiles', blog_views.MDFileViewSet)

urlpatterns = [
    # Examples:
    url(r'^$', 'blog.views.home', name='home'),
    # url(r'^$', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^tag/$', 'blog.views.get_tags', name='get_tags'),
    url(r'^tag/(\S+)/$', 'blog.views.get_list_by_tag', name='get_list_by_tag'),
    url(r'^category/(\S+)/$', 'blog.views.get_list_by_category', name='get_list_by_category'),
    url(r'^about/$', 'blog.views.about_me', name='about-me'),
    url(r'^api-auth/', include('rest_framework.urls',namespace='rest_framework')),
    url(r'^api/', include(router.urls)),

    url(r'^(\S+)/$', 'blog.views.get_blog_by_url', name='get_blog_by_url'),
]


handler404 = "blog.views.page_not_found"
handler500 = "blog.views.server_error"