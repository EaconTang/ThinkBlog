from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(MDFileCategory)


# admin.site.register(MDFileComment)

##
class MDFileAdmin(admin.ModelAdmin):
    list_display = ('md_filename', 'md_url', 'md_pub_time', 'md_mod_time', 'categories', 'tags', 'md_visit', 'md_draft')
    search_fields = ('md_filename', 'md_url')
    list_filter = ('md_pub_time', 'md_category', 'md_tag', 'md_draft')
    list_editable = ('md_filename', 'md_url', 'md_visit')
    list_per_page = 20


admin.site.register(MDFile, MDFileAdmin)


##
class SiteInfoAdmin(admin.ModelAdmin):
    list_display = ('site_version', 'site_visit', 'site_title', 'site_is_published')
    list_editable = ('site_version', 'site_visit', 'site_title', 'site_is_published')


admin.site.register(SiteInfo, SiteInfoAdmin)


##
class MDFileTagAdmin(admin.ModelAdmin):
    list_display = ('md_tag_name', 'blogs_for_tag')


admin.site.register(MDFileTag, MDFileTagAdmin)


##
class MDFileTagURLAdmin(admin.ModelAdmin):
    list_display = ('md_tag_name', 'md_tag_url', 'blogs_for_tagURL')
    list_editable = ('md_tag_name', 'md_tag_url')


admin.site.register(MDFileTagURL, MDFileTagURLAdmin)


##
class MDFileCategoryURLAdmin(admin.ModelAdmin):
    list_display = ('md_category_name', 'md_category_url', 'blogs_for_categoryURL')
    list_editable = ('md_category_name', 'md_category_url')


admin.site.register(MDFileCategoryURL, MDFileCategoryURLAdmin)


#
class WeiboAdmin(admin.ModelAdmin):
    list_display = ('wb_text', 'wb_url', 'wb_pub_time', 'wb_mod_time', 'tags', 'wb_visit', 'wb_draft')
    list_per_page = 20


admin.site.register(Weibo, WeiboAdmin)


#
class WeiboTagAdmin(admin.ModelAdmin):
    list_display = ('wb_tag_name', 'count_weibos_for_tag')
    list_per_page = 20


admin.site.register(WeiboTag, WeiboTagAdmin)


# #
# class ImageFileAdmin(admin.ModelAdmin):
#     list_display = ('image_name', 'image_file', 'is_exported')
#     list_per_page = 10
#
#
# admin.site.register(ImageFile, ImageFileAdmin)

class BackgroundUrlAdmin(admin.ModelAdmin):
    list_display = ('url_name', 'url_full_path', 'url_is_published')
    list_per_page = 20


admin.site.register(BackgroundUrl, BackgroundUrlAdmin)
