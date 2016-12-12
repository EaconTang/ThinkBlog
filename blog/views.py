# coding=utf-8
from __future__ import unicode_literals

from collections import Counter

from django.contrib.sitemaps import Sitemap
from django.http import *
from django.shortcuts import render

from api.utils.export_image_files import mkdir_recursively
from .forms import UploadImageForm
from .models import MDFile, SiteInfo, MDFileCategoryURL, MDFileTagURL, Weibo, BackgroundUrl
from .utils import *

URL_PREFIX = getattr(settings, "URL_PREFIX", "")
STATIC_ARTICLE_PAGE = getattr(settings, "STATIC_ARTICLE_PAGE", False)
STATIC_ARTICLE_PATH = getattr(settings, "STATIC_ARTICLE_PATH", "/static/html/")
STATIC_URL = getattr(settings, "STATIC_URL", "/static/")
STATIC_ROOT = getattr(settings, "STATIC_ROOT")
BASE_DIR = getattr(settings, "BASE_DIR")
BLOG_EACH_PAGE = getattr(settings, "BLOG_EACH_PAGE")
WEIBO_EACH_PAGE = getattr(settings, "WEIBO_EACH_PAGE")


# register = template.Library()
#
#
# @register.simple_tag
# def settings_value(key_name):
#     return getattr(settings, key_name, None)


def home(request):
    return get_blog_list(request)


def get_backgroud_url():
    """"""
    url_obj = BackgroundUrl.objects.get(url_is_published=True)
    return str(url_obj.url_full_path)


def get_archive(request, date_filter=None):
    if not date_filter:
        # archive all
        blog_list = MDFile.objects.exclude(md_draft=True).order_by('-md_pub_time')
        years = (blog.md_pub_time.year for blog in blog_list)
        years_count = Counter(years)
        pub_time_years = sorted(years_count.keys(), reverse=True)
        pub_time_counts = [years_count[y] for y in pub_time_years]
        pub_time_years_display = ['{}年'.format(y) for y in pub_time_years]
        time_counts = zip(pub_time_years, pub_time_years_display, pub_time_counts)
        context = {
            'time_counts': time_counts,
            'blog_list': blog_list,
        }
    else:
        date_list = str(date_filter).rstrip('/').split('/')
        if len(date_list) == 1:
            # archive year
            year = int(date_list[0])
            blog_list = MDFile.objects.exclude(md_draft=True).filter(md_pub_time__year=year).order_by('-md_pub_time')
            months = (blog.md_pub_time.month for blog in blog_list)
            months_count = Counter(months)
            pub_time_months = sorted(months_count.keys(), reverse=True)
            pub_time_counts = [months_count[m] for m in pub_time_months]
            pub_time_months_display = ['{}年{}月'.format(year, m) for m in pub_time_months]
            time_counts = zip(('{}/{}'.format(year, m) for m in pub_time_months), pub_time_months_display,
                              pub_time_counts)
            context = {
                'time_counts': time_counts,
                'blog_list': blog_list,
            }
        elif len(date_list) == 2:
            # archive month
            year, month = map(int, date_list)
            blog_list = MDFile.objects.exclude(md_draft=True).filter(md_pub_time__year=year,
                                                                     md_pub_time__month=month).order_by('-md_pub_time')
            days = [blog.md_pub_time.day for blog in blog_list]
            days_count = Counter(days)
            pub_time_days = sorted(days_count.keys(), reverse=True)
            pub_time_counts = [days_count[d] for d in pub_time_days]
            pub_time_days_display = ['{}年{}月{}日'.format(year, month, day) for day in pub_time_days]
            time_counts = zip(('{}/{}/{}'.format(year, month, d) for d in pub_time_days), pub_time_days_display,
                              pub_time_counts)
            context = {
                'time_counts': time_counts,
                'blog_list': blog_list,
            }
        elif len(date_list) == 3:
            # archive day
            year, month, day = map(int, date_list)
            blog_list = MDFile.objects.exclude(md_draft=True).filter(md_pub_time__year=year,
                                                                     md_pub_time__month=month,
                                                                     md_pub_time__day=day).order_by('-md_pub_time')
            context = {
                'archive_day': True,
                'blog_list': blog_list,
            }
        else:
            return HttpResponseNotFound(b"Not Found!")
    site_info = update_site_visit()
    context.update({
        'url_prefix': URL_PREFIX,
        'site_title': site_info.site_title,
    })
    return render_to_response('archive.html', context)


def get_blog_list(request, page=1):
    """
    :param page:
    :param request:
    :return:
    """
    try:
        page = int(request.GET['page'].strip('/'))
    except:
        page = 1
    blog_counts = MDFile.objects.all().exclude(md_draft=True).count()
    (last_page_num, next_page_num), (index_start, index_end) = paginator(blog_counts, BLOG_EACH_PAGE, int(page))
    blog_list = MDFile.objects.filter(md_draft=False).order_by('-md_pub_time')[index_start - 1: index_end]
    site_info = update_site_visit()
    context = {
        'blog_counts': blog_counts,
        'blog_list': blog_list,
        'site_visit': site_info.site_visit,
        'site_title': site_info.site_title,
        "url_prefix": URL_PREFIX,
        'last_page_num': last_page_num,
        'next_page_num': next_page_num,
        'index_start': index_start,
        'index_end': index_end,
        'bg_url': get_backgroud_url(),

    }
    return render_to_response("blog_list.html", context)


def get_blog_by_url(request, url):
    """
    single blog page html, rendered by markdown
    (unused)static page implementation
    :param request:
    :param url:
    :return:
    """
    # if STATIC_ARTICLE_PAGE:
    #     try:
    #         str_post, year, month, day, title_url = url.split('/')
    #         html_path = os.path.join(STATIC_ARTICLE_PATH, year, month, day, title_url + '.html')
    #         with open(str(BASE_DIR + html_path)) as f:
    #             html_text = f.read()
    #         return HttpResponse(b"{}".format(html_text))
    #     except Exception as e:
    #         pass
    md_object = MDFile.objects.get(md_url=url)

    # check whether URL match date
    year, month, day = str(md_object.md_pub_time.date()).split('-')
    if not str(md_object.md_url).startswith('{}/{}/{}/'.format(year, month, day)):
        # url not match xxxx/xx/xx/title, means maybe new post
        # url not match pub_date, means maybe update post time
        md_object.md_url = '{}/{}/{}/{}'.format(year, month, day, md_object.md_url.split('/')[-1])

    md_text_html = MarkdownRender(md_object.md_text).html
    md_object.md_visit += 1
    md_object.save()

    site_info = update_site_visit()
    context = {
        'article_html': md_text_html,
        'md_object': md_object,
        'site_title': site_info.site_title,
        "url_prefix": URL_PREFIX,
    }

    if md_object.md_draft and not request.user.is_authenticated():
        return render_to_response("404.html", context)
    else:
        return render_to_response("article.html", context)


def get_tags(request):
    """
    blog tags list
    :param request:
    :return:
    """
    all_tags = MDFileTagURL.objects.all()
    # all_tags = [tag for tag in all_tags if not tag.blogs_for_tagURL]
    techblog_category_name = MDFileCategoryURL.objects.get(md_category_url='techblog').md_category_name
    techblog_tags = all_tags.filter(md_tag_name__mdfile__md_category=techblog_category_name).distinct()
    techblog_tags = [t for t in techblog_tags if t.blogs_for_tagURL]
    not_techblog_tags = all_tags.exclude(md_tag_name__mdfile__md_category=techblog_category_name)
    not_techblog_tags = [t for t in not_techblog_tags if t.blogs_for_tagURL]
    site_info = update_site_visit()
    context = {
        "tags": not_techblog_tags,
        "tags_count": len(not_techblog_tags),
        "techblog_tags": techblog_tags,
        "techblog_tags_count": len(techblog_tags),
        "site_title": site_info.site_title,
        "url_prefix": URL_PREFIX,

    }
    return render_to_response("tags.html", context)


def get_list_by_tag(request, tag_url):
    """
    blog list with the tag
    :param request:
    :param tag_url:
    :return:
    """
    try:
        page = int(request.GET['page'].strip('/'))
    except:
        page = 1
    tag_name = MDFileTagURL.objects.get(md_tag_url=tag_url).md_tag_name
    blog_counts = MDFile.objects.filter(md_tag=tag_name).exclude(md_draft=True).count()
    (last_page_num, next_page_num), (index_start, index_end) = paginator(blog_counts, BLOG_EACH_PAGE, page)
    blog_list = MDFile.objects.filter(md_tag=tag_name).exclude(md_draft=True).order_by("-md_pub_time")[
                index_start - 1: index_end]
    site_info = update_site_visit()
    context = {
        'blog_counts': blog_counts,
        'blog_list': blog_list,
        'tag_name': tag_name,
        'tag_url': tag_url,
        "site_title": site_info.site_title,
        "site_visit": site_info.site_visit,
        "url_prefix": URL_PREFIX,
        'last_page_num': last_page_num,
        'next_page_num': next_page_num,
        'index_start': index_start,
        'index_end': index_end,
    }
    return render_to_response("blogs_by_tag.html", context)


def get_list_by_category(request, category_url):
    try:
        page = int(request.GET['page'].strip('/'))
    except:
        page = 1
    category_name = MDFileCategoryURL.objects.get(md_category_url=category_url).md_category_name
    blog_counts = MDFile.objects.filter(md_category=category_name).exclude(md_draft=True).count()
    (last_page_num, next_page_num), (index_start, index_end) = paginator(blog_counts, BLOG_EACH_PAGE, page)
    blog_list = MDFile.objects.filter(md_category=category_name).exclude(md_draft=True).order_by('-md_pub_time')[
                index_start - 1 if index_start != 0 else index_start: index_end]
    site_info = update_site_visit()
    context = {
        'blog_counts': blog_counts,
        'blog_list': blog_list,
        'category_name': category_name,
        'category_url': category_url,
        'site_title': site_info.site_title,
        'site_visit': site_info.site_visit,
        "url_prefix": URL_PREFIX,
        'last_page_num': last_page_num,
        'next_page_num': next_page_num,
        'index_start': index_start,
        'index_end': index_end,
    }
    return render_to_response("blogs_by_category.html", context)


def about_me(request):
    """
    page of 'about', edit in site_info
    :param request:
    :return:
    """
    # html, ok = get_static_page(request)
    # if ok:
    #     return HttpResponse(b"{}".format(html))

    site_info = update_site_visit()
    about_me_html = MarkdownRender(site_info.site_about_me).html
    context = {
        "site_about_me": about_me_html,
        "site_title": site_info.site_title,
        "url_prefix": URL_PREFIX,
        "site_visit": site_info.site_visit,
    }
    return render_to_response("about.html", context)


def get_draft_list(request, draft_type='blog'):
    """
    blogs with 'draft' state, login needed
    :param request:
    :return:
    """
    if draft_type == 'blog':
        return get_draft_blog_list(request)
    if draft_type == 'weibo':
        return get_draft_weibo_list(request)


@Descriptor.ensure_authenticated
def get_draft_blog_list(request):
    """
    :param request:
    :return:
    """
    blog_list = MDFile.objects.filter(md_draft=True).order_by('-md_pub_time')
    site_info = SiteInfo.objects.get(site_is_published=True)
    context = {
        'blog_list': blog_list,
        'site_title': site_info.site_title,
        "url_prefix": URL_PREFIX,
    }
    return render_to_response('draft_blog.html', context)


def get_draft_weibo_list(request):
    """
    :param request:
    :return:
    """
    return render_to_response('404.html', {})


def page_not_found(request):
    """standard 404 error page"""
    context = {
        "url_prefix": URL_PREFIX,
    }
    return render_to_response("404.html", context)


def server_error(request):
    """standard 500 error page"""
    context = {
        "url_prefix": URL_PREFIX,
    }
    return render_to_response("500.html", context)


# class MDFileViewSet(viewsets.ModelViewSet):
#     queryset = MDFile.objects.all().exclude(md_draft=True).order_by('-md_pub_time')
#     serializer_class = MDFileSerializer


class BlogSitemap(Sitemap):
    """
    (unused)sitemap
    """
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return MDFile.objects.filter(md_draft=False)

    def location(self, obj):
        return URL_PREFIX + '/post' + obj.md_url


def get_weibo_list(request):
    """
    weibo list, each page show counts WEIBO_EACH_PAGE, each weibo is rendered by markdown
    :param request:
    :return:
    """
    try:
        page = int(request.GET['page'].strip('/'))
    except:
        page = 1
    weibo_counts = Weibo.objects.filter(wb_draft=False).count()
    (last_page_num, next_page_num), (index_start, index_end) = paginator(weibo_counts, WEIBO_EACH_PAGE, page)

    weibo_object_list = Weibo.objects.filter(wb_draft=False).order_by('-wb_pub_time')[index_start - 1: index_end]
    weibo_html_list = [MarkdownRender(wb.wb_text).html for wb in weibo_object_list]

    # gather weibo_object and weibo_html to a dict_list
    weibo_list = list()
    for wb, wb_html in zip(weibo_object_list, weibo_html_list):
        _d = {
            'wb_object': wb,
            'wb_html': wb_html
        }
        weibo_list.append(_d)

    site_info = update_site_visit()
    context = {
        'weibo_list': weibo_list,
        'weibo_counts': weibo_counts,
        'site_title': site_info.site_title,
        'url_prefix': URL_PREFIX,
        'last_page_num': last_page_num,
        'next_page_num': next_page_num,
        'index_start': index_start,
        'index_end': index_end,
    }
    return render_to_response('weibo_list.html', context)


def get_weibo_by_url(request, url):
    """
    single weibo page html, rendered by markdown
    :param request:
    :param url:
    :return:
    """
    _weibo = Weibo.objects.get(wb_url=url)
    weibo_html = MarkdownRender(_weibo.wb_text).html
    site_info = update_site_visit()
    context = {
        'wb_pub_time': _weibo.wb_pub_time,
        'weibo_html': weibo_html,
        'site_title': site_info.site_title,
        'url_prefix': URL_PREFIX,
    }
    if _weibo.wb_draft and not request.user.is_authenticated():
        return render_to_response("404.html", context)
    else:
        return render_to_response("weibo.html", context)


@Descriptor.ensure_authenticated
def upload_file(request, file_type):
    """
    upload file, usually saved in /static/
    :param request:
    :param file_type:
    :return:
    """
    if str(file_type) == 'image':
        return upload_image(request)
    else:
        return HttpResponseNotFound(content=b"No such type file could be upload!")


def upload_image(request):
    """
    upload image to specific path
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            image_file, image_title, image_dir = request.FILES['image_file'], form.cleaned_data['image_name'], \
                                                 form.cleaned_data['image_dir']
            if image_dir:
                image_full_path = os.path.join(image_dir, image_title)
            else:
                image_full_path = os.path.join(STATIC_ROOT, 'image', image_title)
            image_dir = os.path.dirname(image_full_path)
            if not os.path.exists(image_dir) or os.path.isfile(image_dir):
                mkdir_recursively(image_dir)

            with open(image_full_path, 'wb+') as f:
                for chunk in image_file.chunks():
                    f.write(chunk)
            return render(request, 'upload_image.html', {'result_success': 'Upload_success!', 'form': form})
        else:
            return HttpResponse(b"Form is invalid!")
    else:
        form = UploadImageForm()
        return render(request, 'upload_image.html', {'form': form})


def browse_file(request, path):
    """
    browse static files
    :param request:
    :param path:
    :return:
    """
    if str(path).startswith('image'):
        return view_image(request, path)
    else:
        return HttpResponseNotFound(content=b"No such file for browsing!")


def view_image(request, path='image'):
    """
    view images under specific path
    :param request:
    :param path:
    :return:
    """
    image_path = os.path.join(STATIC_ROOT, path)
    files_n_dirs = [_ for _ in os.listdir(image_path) if not str(_).startswith('.')]
    image_file_list = [_ for _ in files_n_dirs if os.path.isfile(os.path.join(image_path, _))]
    image_dir_list = [_ for _ in files_n_dirs if os.path.isdir(os.path.join(image_path, _))]
    context = {
        'request_path': path,
        'image_file_list': image_file_list,
        'image_dir_list': image_dir_list,
        'url_prefix': URL_PREFIX,
    }
    return render_to_response('view_image.html', context)


@Descriptor.ensure_authenticated
def api_utils(request, api):
    """
    api utils
    :param request:
    :param api:
    :return:
    """
    try:
        if api == 'export-mdfiles':
            from api.utils.export_mdfiles import main as export_mdfiles
            export_mdfiles()
            return HttpResponse(b"OK!")
        elif api == 'test':
            return HttpResponse(b"OK! This is a test api!")
        elif api == 'export-image':
            from api.utils.export_image_files import main as export_image
            export_image()
            return HttpResponse(b"OK! All images in database is exported!")
        else:
            return Http404
    except Exception:
        raise


@Descriptor.ensure_authenticated
def display_meta(request):
    values = request.META.items()
    html = ['<tr><td>%s</td><td>%s</td></tr>' % (k, v) for k, v in sorted(values)]
    return HttpResponse('<table>%s</table>' % '\n'.join(html))


def get_sitemap(request):
    """
    sitemap.xml, if last modify time larger than 1-week, create a new one
    :param request:
    :return:
    """
    sitemap_file = os.path.join(BASE_DIR, 'sitemap.xml')

    # pysitemap bug, use crontab
    # ----------
    # try:
    #     mtime = os.stat(sitemap_file).st_mtime
    #     if time.time() - mtime > 60 * 60 * 24 * 7:
    #         raise Exception('Sitemap.xml out of date!')
    # except:
    #     crawler = pysitemap.Crawler(url='http://blog.tangyingkang.com/',
    #                                 outputfile=sitemap_file,
    #                                 logfile='/var/log/sitemap.log',
    #                                 oformat='xml')
    #     crawler.crawl()

    with open(sitemap_file) as f:
        sitemap_xml = f.read()
    return HttpResponse(sitemap_xml)
