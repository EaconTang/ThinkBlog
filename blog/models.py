# coding=utf-8

from django.db import models
from .utils import markdown_syntax
from datetime import datetime

class SiteInfo(models.Model):
    """
    site info, mainly of: site title/site visit/about me page
    """
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
    """
    category name
    """
    md_category_name = models.CharField(verbose_name="CategoryName", max_length=32, unique=True)

    def __unicode__(self):
        return self.md_category_name

    class Meta:
        verbose_name_plural = verbose_name = "分类"

    @property
    def blogs_for_category(self):
        return self.mdfile_set.all().exclude(md_draft=True).count()


class MDFileCategoryURL(models.Model):
    """
    url for category name
    """
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
    """
    tag name
    """
    md_tag_name = models.CharField(verbose_name="TagName", max_length=32, unique=True)

    def __unicode__(self):
        return self.md_tag_name

    class Meta:
        verbose_name_plural = verbose_name = "标签"

    @property
    def blogs_for_tag(self):
        return self.mdfile_set.all().exclude(md_draft=True).count()


class MDFileTagURL(models.Model):
    """
    url for tag name
    """
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
    """
    (core model)
    blog model, each blog is modeled as a md file, which contains much meta info
    """
    md_url = models.CharField(verbose_name="URL", max_length=256, unique=True)
    md_filename = models.CharField(verbose_name="Title", max_length=128, unique=True)
    md_text = models.TextField(verbose_name="Text", blank=True, help_text=markdown_syntax())
    md_pub_time = models.DateTimeField(verbose_name='Publish Time', null=True)
    md_mod_time = models.DateTimeField(verbose_name='Modify Time', null=True, auto_now=True)
    # md_modified = models.NullBooleanField()
    md_visit = models.IntegerField(verbose_name="Visits", null=True, default=0)
    md_category = models.ManyToManyField(MDFileCategory, verbose_name="Category", null=True, default="uncategorized")
    md_tag = models.ManyToManyField(MDFileTag, verbose_name="Tag", null=True, default="untagged")
    md_summary = models.TextField(blank=True)
    md_draft = models.NullBooleanField(default=False)
    md_catalogue = models.NullBooleanField(default=False)
    md_keywords = models.CharField(verbose_name="Keywords", max_length=128, blank=True)

    def __unicode__(self):
        return self.md_filename

    class Meta:
        verbose_name_plural = verbose_name = "博客"
        get_latest_by = "-md_pub_time"
        ordering = ['-md_pub_time', ]

    @property
    def tags(self):
        """
        :return: tags of a blog to be displayed in django-admin
        """
        return '/'.join(str(tag) for tag in self.md_tag.all())

    @property
    def tags_list(self):
        return self.tags.split('/')

    @property
    def categories(self):
        return '/'.join(str(catgr) for catgr in self.md_category.all())


class WeiboTag(models.Model):
    """
    tag for weibo
    """
    wb_tag_name = models.CharField(verbose_name="WeiboTagName", max_length=32, unique=True)

    def __unicode__(self):
        return self.wb_tag_name

    class Meta:
        verbose_name_plural = verbose_name = "微博标签"

    @property
    def weibos_for_tag(self):
        return self.weibo_set.all().exclude(wb_draft=True)

    @property
    def count_weibos_for_tag(self):
        return self.weibos_for_tag.count()


class Weibo(models.Model):
    """
    (core model)
    weibo model, each weibo is also modeled as md file, but with less meta info
    """
    wb_url = models.AutoField(primary_key=True)
    wb_text = models.TextField(verbose_name="WeiboText", default='Default text.')
    wb_pub_time = models.DateTimeField(verbose_name='Publish Time', null=True, default=datetime.now)
    wb_mod_time = models.DateTimeField(verbose_name='Modify Time', null=True, auto_now=True)
    wb_visit = models.IntegerField(verbose_name="Visits", null=True, default=0)
    wb_tag = models.ManyToManyField(WeiboTag, verbose_name="Tag", blank=True, null=True, default="untagged")
    wb_draft = models.NullBooleanField(default=False)

    def __unicode__(self):
        return self.wb_text[:64]

    class Meta:
        verbose_name_plural = verbose_name = '微博'
        get_latest_by = '-wb_pub_time'
        ordering = ['-wb_pub_time', ]

    @property
    def tags(self):
        return '/'.join(str(tag) for tag in self.wb_tag.all())


# class MDFileComment(models.Model):
#     md_comment_author = models.CharField(max_length=32, default="Anonymous", blank=True)
#     md_comment_mail = models.EmailField(blank=True)
#     md_comment_time = models.DateTimeField('comment time', null=True)
#     md_comment = models.TextField()
#     md_file = models.ForeignKey(MDFile, on_delete=models.CASCADE, null=True)
#
#     def __unicode__(self):
#         return self.id
#
#     class Meta:
#         verbose_name_plural = verbose_name = "评论"
#         abstract = True
#
#
# class DuoshuoComment(MDFileComment):
#     pass
#
#
# class DisqusComment(MDFileComment):
#     pass


# register = template.Library()
#
#
# @register.simple_tag
# def settings_value(key_name):
#     return getattr(settings, key_name, None)


class ImageFile(models.Model):
    image_file = models.ImageField(verbose_name='ImageFile')
    image_name = models.CharField(verbose_name='ImageName', max_length=32)

    # static_image_path = os.path.join(getattr(settings, 'STATIC_ROOT'), 'image')
    # files_n_dirs = (_ for _ in os.listdir(static_image_path) if not str(_).startswith('.'))
    # image_dir_list = (_ for _ in files_n_dirs if os.path.isdir(os.path.join(static_image_path, _)))
    # image_path = models.CharField(choices=files_n_dirs, verbose_name='ImageDirectory', max_length=64)

    # ttl = models.DateTimeField(verbose_name='ImageTTL')
    is_exported = models.BooleanField(default=False)


class BackgroundUrl(models.Model):
    url_full_path = models.URLField(verbose_name='BackgroundURL')
    url_name = models.CharField(verbose_name='URLName', max_length=128)
    url_is_published = models.NullBooleanField(verbose_name="Published", default=False)

    def __unicode__(self):
        return self.url_name

    class Meta:
        verbose_name_plural = verbose_name = '背景图片'
