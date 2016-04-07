# coding=utf-8
from django.db import models
from .utils import markdown_syntax
from django import template
from django.conf import settings


class SiteInfo(models.Model):
    site_version = models.CharField(verbose_name="Site Version", default="0.0", max_length=32)
    site_title = models.CharField(verbose_name="Site Title", blank=True, max_length=32)
    site_visit = models.IntegerField(verbose_name="Site Visits", default=0)
    site_copyright = models.TextField(verbose_name="Site copyright", null=True)
    site_about_me = models.TextField(verbose_name="About Me", blank=True)
    site_is_published = models.NullBooleanField(verbose_name="Published", default=False)

    def __unicode__(self):
        return self.site_version

    class Meta:
        verbose_name_plural = verbose_name = "网站信息"


class MDFileCategory(models.Model):
    md_category_name = models.CharField(verbose_name="CategoryName", max_length=32, unique=True)

    def __unicode__(self):
        return self.md_category_name

    class Meta:
        verbose_name_plural = verbose_name = "分类"

    @property
    def blogs_for_category(self):
        return self.mdfile_set.all().exclude(md_draft=True).count()


class MDFileCategoryURL(models.Model):
    md_category_url = models.CharField(max_length=64)
    md_category_name = models.OneToOneField(MDFileCategory)

    def __unicode__(self):
        return self.md_category_url

    class Meta:
        verbose_name_plural = verbose_name = "分类-网址"

    @property
    def blogs_for_categoryURL(self):
        return self.md_category_name.blogs_for_category


class MDFileTag(models.Model):
    md_tag_name = models.CharField(verbose_name="TagName", max_length=32, unique=True)

    def __unicode__(self):
        return self.md_tag_name

    class Meta:
        verbose_name_plural = verbose_name = "标签"

    @property
    def blogs_for_tag(self):
        return self.mdfile_set.all().exclude(md_draft=True).count()


class MDFileTagURL(models.Model):
    md_tag_name = models.OneToOneField(MDFileTag)
    md_tag_url = models.CharField(max_length=64)

    def __unicode__(self):
        return self.md_tag_url

    class Meta:
        verbose_name_plural = verbose_name = "标签-网址"

    @property
    def blogs_for_tagURL(self):
        return self.md_tag_name.blogs_for_tag


class MDFile(models.Model):
    md_url = models.CharField(verbose_name="URL", max_length=256, unique=True)
    md_filename = models.CharField(verbose_name="Title", max_length=128, unique=True)
    md_text = models.TextField(verbose_name="Text", blank=True, help_text=markdown_syntax())
    md_pub_time = models.DateTimeField(verbose_name='Publish Time', null=True)
    md_mod_time = models.DateTimeField(verbose_name='Modify Time', null=True, auto_now=True)
    md_modified = models.NullBooleanField()
    md_visit = models.IntegerField(verbose_name="Visits", null=True)
    md_category = models.ManyToManyField(MDFileCategory, verbose_name="Category", null=True, default="uncategorized")
    md_tag = models.ManyToManyField(MDFileTag, verbose_name="Tag", null=True, default="untagged")
    md_summary = models.TextField(blank=True)
    md_draft = models.NullBooleanField(default=False)

    def __unicode__(self):
        return self.md_filename

    class Meta:
        verbose_name_plural = verbose_name = "博客"

    @property
    def tags(self):
        """
        :return: tags of a blog to be displayed in django-admin
        """
        return '/'.join([str(tag) for tag in self.md_tag.all()])

    @property
    def categories(self):
        return '/'.join([str(catgr) for catgr in self.md_category.all()])


class MDFileComment(models.Model):
    md_comment_author = models.CharField(max_length=32, default="Anonymous", blank=True)
    md_comment_mail = models.EmailField(blank=True)
    md_comment_time = models.DateTimeField('comment time', null=True)
    md_comment = models.TextField()
    md_file = models.ForeignKey(MDFile, on_delete=models.CASCADE, null=True)

    def __unicode__(self):
        return self.id

    class Meta:
        verbose_name_plural = verbose_name = "评论"


register = template.Library()


@register.simple_tag
def settings_value(key_name):
    return getattr(settings, key_name, None)