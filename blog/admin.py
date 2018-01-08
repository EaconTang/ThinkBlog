# coding=utf-8
from django.contrib import admin
from django.contrib.admin import AdminSite

from .models import *


class MyAdminSite(AdminSite):
    """这里修改后台登录页面的标题文字显示，比直接修改"django.contrib.admin.templates.admin.base_site.html"更好"""
    site_title = "ThinkBlog"
    site_header = "ThinkBlog"


my_admin_site = MyAdminSite()


# Register your models here.
my_admin_site.register(MDFileCategory)


# my_admin_site.register(MDFileComment)

##
class MDFileAdmin(admin.ModelAdmin):
    list_display = ('md_filename', 'md_url', 'md_pub_time', 'md_mod_time', 'categories', 'tags', 'md_visit', 'md_draft')
    search_fields = ('md_filename', 'md_url')
    list_filter = ('md_pub_time', 'md_category', 'md_tag', 'md_draft')
    list_editable = ('md_filename', 'md_url', 'md_visit')
    list_per_page = 20


my_admin_site.register(MDFile, MDFileAdmin)


##
class SiteInfoAdmin(admin.ModelAdmin):
    list_display = ('site_version', 'site_visit', 'site_title', 'site_is_published')
    list_editable = ('site_version', 'site_visit', 'site_title', 'site_is_published')


my_admin_site.register(SiteInfo, SiteInfoAdmin)


class SiteVisitAdmin(admin.ModelAdmin):
    list_display = ('time_visit', 'site_visit', 'day_visit', 'month_visit')
    list_editable = ('site_visit',)


my_admin_site.register(SiteVisit, SiteVisitAdmin)


##
class MDFileTagAdmin(admin.ModelAdmin):
    list_display = ('md_tag_name', 'blogs_for_tag')


my_admin_site.register(MDFileTag, MDFileTagAdmin)


##
class MDFileTagURLAdmin(admin.ModelAdmin):
    list_display = ('md_tag_name', 'md_tag_url', 'blogs_for_tagURL')
    list_editable = ('md_tag_name', 'md_tag_url')


my_admin_site.register(MDFileTagURL, MDFileTagURLAdmin)


##
class MDFileCategoryURLAdmin(admin.ModelAdmin):
    list_display = ('md_category_name', 'md_category_url', 'blogs_for_categoryURL')
    list_editable = ('md_category_name', 'md_category_url')


my_admin_site.register(MDFileCategoryURL, MDFileCategoryURLAdmin)


#
class WeiboAdmin(admin.ModelAdmin):
    list_display = ('wb_text', 'wb_url', 'wb_pub_time', 'wb_mod_time', 'tags', 'wb_visit', 'wb_draft')
    list_per_page = 20


my_admin_site.register(Weibo, WeiboAdmin)


#
class WeiboTagAdmin(admin.ModelAdmin):
    list_display = ('wb_tag_name', 'count_weibos_for_tag')
    list_per_page = 20


my_admin_site.register(WeiboTag, WeiboTagAdmin)


class BackgroundUrlAdmin(admin.ModelAdmin):
    list_display = ('url_name', 'url_full_path', 'url_is_published')
    list_per_page = 20


my_admin_site.register(BackgroundUrl, BackgroundUrlAdmin)
