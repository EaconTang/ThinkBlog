from django.conf.urls import include, url
from django.contrib import admin

# from rest_framework import routers

# router = routers.DefaultRouter()
# router.register(r'mdfiles', blog_views.MDFileViewSet)

urlpatterns = [
    url(r'^$', 'blog.views.home', name='home'),
    # url(r'^$', include('blog.urls')),

    # admin
    url(r'^admin/', include(admin.site.urls)),

    # blog post
    url(r'^post/(\S+)/$', 'blog.views.get_blog_by_url', name='get_blog_by_url'),
    url(r'^tag/$', 'blog.views.get_tags', name='get_tags'),
    url(r'^tag/(\S+)/$', 'blog.views.get_list_by_tag', name='get_list_by_tag'),
    url(r'^category/(\S+)/$', 'blog.views.get_list_by_category', name='get_list_by_category'),
    url(r'^draft/(\S+)/$', 'blog.views.get_draft_list', name='get_draft_list'),
    # url(r'^archive/$', 'blog.views.get_archive', name='get_archive'),
    url(r'^archive/(\S*)$', 'blog.views.get_archive', name='get_archive'),

    url(r'^about/$', 'blog.views.about_me', name='about-me'),

    # url(r'^api-auth/', include('rest_framework.urls',namespace='rest_framework')),
    # url(r'^api/', include(router.urls)),
    # url(r'^api/utils/(\S+)/$', 'blog.views.api_utils', name='api_utils'),

    # account
    url(r'^account/', include('django.contrib.auth.urls')),

    # sitemap
    url(r'^sitemap\.xml$', 'blog.views.get_sitemap', name='get_sitemap'),

    # weibo
    url(r'^weibo/$', 'blog.views.get_weibo_list', name='get_weibo_list'),
    url(r'^weibo/(\S+)/$', 'blog.views.get_weibo_by_url', name='get_weibo_by_url'),

    # file upload
    url('^upload/(\S+)/$', 'blog.views.upload_file', name='upload_file'),
    url('^browse/(\S+)/$', 'blog.views.browse_file', name='browse_file'),

    # url('^display-meta/$', 'blog.views.display_meta', name='display_meta'),

    # site visit
    url('^statistic/site-visit/$', 'blog.views.get_site_visit', name='site_visit'),
    # url('^statistic/blog-visit/$', 'blog.views.get_blog_visit', name='blog_visit'),

]

handler404 = "blog.views.page_not_found"
handler500 = "blog.views.server_error"
