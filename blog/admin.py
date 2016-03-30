from django.contrib import admin
from .models import MDFile, MDFileCategory, MDFileTag, MDFileComment

# Register your models here.
admin.site.register(MDFile)
admin.site.register(MDFileCategory)
admin.site.register(MDFileTag)
admin.site.register(MDFileComment)
