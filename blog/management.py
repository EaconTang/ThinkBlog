# coding=utf-8
"""数据库初始化"""

from django.db.models.signals import post_migrate
from blog.models import *


def init_db(sender, **kwargs):
    if sender.name == 'blog':
        if not SiteInfo.objects.exists():
            SiteInfo.objects.create(
                site_version='0.0',
                site_title='ThinkBlog',
                site_visit=0,
                site_copyright='Developed by <a href="http://www.tangyingkang.com">Eacon</a>|Powered by <a href="https://www.djangoproject.com/">Django</a>',
                site_about_me='About me.',
                site_is_published=True
            )
            print "Init model: SiteInfo..."
        if not MDFileCategory.objects.exists():
            MDFileCategory.objects.create(
                md_category_name='技术博客'
            )
            print "Init model: MDFileCategory..."
        if not MDFileCategoryURL.objects.exists():
            MDFileCategoryURL.objects.create(
                md_category_url='techblog',
                md_category_name=MDFileCategory.objects.get(md_category_name='技术博客')
            )
            print "Init model: MDFileCategoryURL..."


post_migrate.connect(init_db)