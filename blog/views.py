# coding=utf-8
from __future__ import unicode_literals
from django.shortcuts import render_to_response
import markdown2
from .utils import MDResponse, MarkdownRender
from .models import MDFile, SiteInfo, MDFileCategoryURL, MDFileTagURL
from MyBlog import settings


def home(request, version="online"):
    blog_list = MDFile.objects.all().order_by('-md_pub_time')
    site_info = SiteInfo.objects.get(site_version=version)
    site_info.site_visit += 1
    context = {
        'blog_list': blog_list,
        'site_visit': site_info.site_visit,
        'site_title': settings.SITE_TITLE,
    }
    site_info.save()
    return render_to_response("home.html", context)


def get_by_name(request, filename):
    md_text = MDFile.objects.get(md_filename=filename).md_text
    return MDResponse(md_text=md_text)


def get_blog_by_url(request, url):
    md_object = MDFile.objects.get(md_url=url)
    md_text = md_object.md_text
    article_body = markdown2.markdown(md_text)
    context = {
        'article_html': article_body,
        "article_md_text": md_text,
        'article_md_object': md_object,
        'site_title': settings.SITE_TITLE,
    }

    return render_to_response("article.html", context)


def get_tags(request):
    all_tags = MDFileTagURL.objects.all()
    context = {
        "tags": all_tags,
        "site_title": settings.SITE_TITLE,
    }
    return render_to_response("tags.html", context)


def get_list_by_tag(request, tag_url):
    tag_name = MDFileTagURL.objects.get(md_tag_url=tag_url).md_tag_name
    blog_list = MDFile.objects.filter(md_tag=tag_name).order_by("-md_pub_time")
    context = {
        'blog_list': blog_list,
        'tag_name': tag_name,
        "site_title": settings.SITE_TITLE,
    }
    return render_to_response("blogs_by_tag.html", context)


def get_list_by_category(request, category_url):
    category_name = MDFileCategoryURL.objects.get(md_category_url=category_url).md_category_name
    blog_list = MDFile.objects.filter(md_category=category_name).order_by('-md_pub_time')
    context = {
        'blog_list': blog_list,
        'category_name': category_name,
        'site_title': settings.SITE_TITLE,
    }
    return render_to_response("blogs_by_category.html", context)