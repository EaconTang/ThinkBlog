from django.contrib import admin
from .models import MDFile, MDFileCategory, MDFileCategoryURL, MDFileTag, MDFileTagURL, MDFileComment, SiteInfo

# Register your models here.
admin.site.register(MDFileCategory)
admin.site.register(MDFileCategoryURL)
# admin.site.register(MDFileComment)


class MDFileAdmin(admin.ModelAdmin):
    list_display = ('md_filename', 'md_url', 'md_pub_time', 'md_mod_time', 'categories', 'tags', 'md_visit', 'md_draft')
    search_fields = ('md_filename',)
    list_filter = ('md_pub_time', 'md_category', 'md_tag', 'md_draft')
    list_editable = ('md_filename', 'md_url', 'md_visit')
    list_per_page = 20

admin.site.register(MDFile, MDFileAdmin)


class SiteInfoAdmin(admin.ModelAdmin):
    list_display = ('site_version', 'site_visit', 'site_title', 'site_is_published')
    list_editable = ('site_version', 'site_visit', 'site_title', 'site_is_published')

admin.site.register(SiteInfo, SiteInfoAdmin)


class MDFileTagAdmin(admin.ModelAdmin):
    list_display = ('md_tag_name', 'blogs_for_tag')

admin.site.register(MDFileTag, MDFileTagAdmin)


class MDFileTagURLAdmin(admin.ModelAdmin):
    list_display = ('md_tag_name', 'md_tag_url', 'blogs_for_tagURL')
    list_editable = ('md_tag_name', 'md_tag_url')

admin.site.register(MDFileTagURL, MDFileTagURLAdmin)


class MDFileCategoryURLAdmin(admin.ModelAdmin):
    list_display = ('md_category_name', 'md_category_url', 'blogs_for_categoryURL')
    list_editable = ('md_category_name', 'md_category_url')
