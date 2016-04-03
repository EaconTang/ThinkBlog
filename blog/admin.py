from django.contrib import admin
from .models import MDFile, MDFileCategory, MDFileCategoryURL, MDFileTag, MDFileTagURL, MDFileComment, SiteInfo

# Register your models here.
admin.site.register(MDFileCategory)
admin.site.register(MDFileCategoryURL)
admin.site.register(MDFileTag)
admin.site.register(MDFileTagURL)
admin.site.register(MDFileComment)


class MDFileAdmin(admin.ModelAdmin):
    list_display = ('md_filename', 'md_url', 'md_pub_time', 'md_mod_time', 'categories', 'tags', 'md_visit',)
    search_fields = ('md_filename',)
    list_filter = ('md_pub_time', 'md_category', 'md_tag')

admin.site.register(MDFile, MDFileAdmin)


class SiteInfoAdmin(admin.ModelAdmin):
    list_display = ('site_version', 'site_visit', 'site_copyright')

admin.site.register(SiteInfo, SiteInfoAdmin)