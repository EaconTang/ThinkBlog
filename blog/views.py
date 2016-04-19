# coding=utf-8
from __future__ import unicode_literals
from django.shortcuts import render_to_response
from .utils import MarkdownResponse, MarkdownRender
from .models import MDFile, SiteInfo, MDFileCategoryURL, MDFileTagURL
from django import template
from django.conf import settings
from rest_framework import viewsets
from .serializers import MDFileSerializer


URL_PREFIX = getattr(settings, "URL_PREFIX", "")
# SITE_INFO = SiteInfo.objects.get(site_is_published=True)
register = template.Library()


@register.simple_tag
def settings_value(key_name):
    return getattr(settings, key_name, None)


def home(request):
    blog_list = MDFile.objects.all().exclude(md_draft=True).order_by('-md_pub_time')
    blog_counts = blog_list.count()
    site_info = SiteInfo.objects.get(site_is_published=True)
    site_info.site_visit += 1
    site_info.save()
    context = {
        'blog_list': blog_list,
        'blog_counts': blog_counts,
        'site_visit': site_info.site_visit,
        'site_title': site_info.site_title,
        "url_prefix": URL_PREFIX,
    }
    return render_to_response("home.html", context)


def get_by_name(request, filename):
    md_text = MDFile.objects.get(md_filename=filename).md_text
    return MarkdownResponse(md_text=md_text)


def get_blog_by_url(request, url):
    md_object = MDFile.objects.get(md_url=url)
    md_text = md_object.md_text
    article_body = MarkdownRender(md_text).html
    md_object.md_visit += 1
    md_object.save()
    site_info = SiteInfo.objects.get(site_is_published=True)
    site_info.site_visit += 1
    site_info.save()
    context = {
        'article_html': article_body,
        'article_md_object': md_object,
        'site_title': site_info.site_title,
        "url_prefix": URL_PREFIX,
    }

    return render_to_response("article.html", context)


def get_tags(request):
    all_tags = MDFileTagURL.objects.all()
    tags_counts = all_tags.count()
    site_info = SiteInfo.objects.get(site_is_published=True)
    site_info.site_visit += 1
    site_info.save()
    context = {
        "tags": all_tags,
        "tags_counts": tags_counts,
        "site_title": site_info.site_title,
        "site_visit": site_info.site_visit,
        "url_prefix": URL_PREFIX,

    }
    return render_to_response("tags.html", context)


def get_list_by_tag(request, tag_url):
    tag_name = MDFileTagURL.objects.get(md_tag_url=tag_url).md_tag_name
    blog_list = MDFile.objects.filter(md_tag=tag_name).exclude(md_draft=True).order_by("-md_pub_time")
    blog_counts = blog_list.count()
    site_info = SiteInfo.objects.get(site_is_published=True)
    site_info.site_visit += 1
    site_info.save()
    context = {
        'blog_list': blog_list,
        'blog_counts': blog_counts,
        'tag_name': tag_name,
        "site_title": site_info.site_title,
        "site_visit": site_info.site_visit,
        "url_prefix": URL_PREFIX,
    }
    return render_to_response("blogs_by_tag.html", context)


def get_list_by_category(request, category_url):
    category_name = MDFileCategoryURL.objects.get(md_category_url=category_url).md_category_name
    blog_list = MDFile.objects.filter(md_category=category_name).exclude(md_draft=True).order_by('-md_pub_time')
    blog_counts = blog_list.count()
    site_info = SiteInfo.objects.get(site_is_published=True)
    site_info.site_visit += 1
    site_info.save()
    context = {
        'blog_list': blog_list,
        'blog_counts': blog_counts,
        'category_name': category_name,
        'site_title': site_info.site_title,
        'site_visit': site_info.site_visit,
        "url_prefix": URL_PREFIX,
    }
    return render_to_response("blogs_by_category.html", context)


def about_me(request):
    site_info = SiteInfo.objects.get(site_is_published=True)
    about_me_html = MarkdownRender(site_info.site_about_me).html
    site_info.site_visit += 1
    site_info.save()
    context = {
        "site_about_me": about_me_html,
        "site_title": site_info.site_title,
        "url_prefix": URL_PREFIX,
        "site_visit": site_info.site_visit,
    }

    return render_to_response("about.html", context)


def page_not_found(request):
    context = {
        "url_prefix": URL_PREFIX,
    }
    return render_to_response("404.html", context)


def server_error(request):
    context = {
        "url_prefix": URL_PREFIX,
    }
    return render_to_response("500.html", context)


class MDFileViewSet(viewsets.ModelViewSet):
    queryset = MDFile.objects.all().exclude(md_draft=True).order_by('-md_pub_time')
    serializer_class = MDFileSerializer
