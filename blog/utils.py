# coding=utf-8
"""
custom class and function
"""
import HTMLParser
import re
import os
import inspect
import time
from functools import wraps
from datetime import datetime

import markdown
import requests
from django.conf import settings
from django.shortcuts import HttpResponse, render_to_response, Http404
from pygments import highlight, lexers
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import *

STATIC_ROOT = getattr(settings, 'STATIC_ROOT')
BASE_DIR = getattr(settings, 'BASE_DIR')


def html_response(*args, **kwargs):
    return render_to_response(*args, **kwargs)


class MarkdownResponse(HttpResponse):
    """
    django http-response with markdown-rendered html
    """

    def __init__(self, md_text='', *args, **kwargs):
        super(HttpResponse, self).__init__(*args, **kwargs)
        self.content = MarkdownRender(md_text).html


class MarkdownRender(object):
    """
    markdown renderer, trans md_text to html
    """

    def __init__(self, text):
        self._html = markdown.markdown(text)
        if '<pre><code>' in self._html:
            self._html = CodeHighlighter(self._html).html

    @property
    def html(self):
        return self._html


class CodeHighlighter(object):
    """
    heightlight the code in html
    using pygments
    """

    def __init__(self, html, height_lighter='pygments', code_language=None):
        self._html = str(html)
        self.code_language = code_language
        if height_lighter != 'pygments':
            raise NotImplementedError

    @property
    def code_blocks(self):
        _pattern = r'<pre><code>(.*?)</code></pre>'
        p = re.compile(_pattern, flags=re.S)
        return p.findall(self._html)

    def light_block(self, code_block):
        code_block = HTMLParser.HTMLParser().unescape(code_block)
        try:
            if self.code_language:
                lexer = get_lexer_by_name(self.code_language, stripall=True)
            else:
                lexer = lexers.guess_lexer(str(code_block).strip(), stripall=True)
        except:
            lexer = get_lexer_by_name('python', stripall=True)
        # formatter = HtmlFormatter(linenos='inline')
        formatter = HtmlFormatter()
        return highlight(code_block, lexer, formatter)

    @property
    def html(self):
        blocks = self.code_blocks
        lighted_blocks = [self.light_block(b) for b in blocks]
        blocks = ['<pre><code>{}</code></pre>'.format(b) for b in blocks]
        for i in range(len(blocks)):
            self._html = self._html.replace(blocks[i], lighted_blocks[i])
        return self._html


def markdown_syntax():
    """
    used as blog editor's hint in django-admin-UI
    :return:
    """
    return """
    Markdown语法说明: http://www.jianshu.com/p/q81RER
    """


def update_site_visit(add=1, sub=0):
    """
    update site_visit, default to add 1 each time when called
    :param add:
    :param sub:
    :return:
    """
    try:
        from .models import SiteInfo, SiteVisit
        site_info = SiteInfo.objects.get(site_is_published=True)
        site_info.site_visit += add
        site_info.site_visit -= sub
        site_info.save()

        # site visit for each hour
        c_hour = datetime_hour_now()
        site_visit = SiteVisit.objects.get_or_create(time_visit=c_hour,
                                                     day_visit=c_hour.date(),
                                                     month_visit=c_hour.strftime('%Y-%m'))[0]
        site_visit.site_visit += add
        site_visit.site_visit -= sub
        site_visit.save()
    except Exception:
        raise
    else:
        return site_info


def datetime_hour_now():
    """
    :return: current hour
    """
    ct = int(time.time())
    ct -= ct % ( 60 * 60)
    return datetime.fromtimestamp(ct)


def mkdir_recursively(dir_path):
    """
    create directory recursively
    :param dir_path:
    :return:
    """
    while True:
        try:
            os.mkdir(dir_path)
        except OSError:
            parent_dir = os.path.dirname(dir_path)
            if mkdir_recursively(parent_dir):
                continue
        else:
            break
    return True


def paginator(num_all, num_each_page, current_page_num):
    """
    custom paginator, return page_num and index for frontend(not for python list index)
    :param num_all:
    :param num_each_page:
    :param current_page_num:
    :return:
    """
    if num_all == 0:
        return (1, 1), (0, 0)
    # compute the page_num of last page and next page
    div, mod = divmod(num_all, int(num_each_page))
    page_counts = div if mod == 0 else div + 1
    last_page_num = current_page_num - 1 if current_page_num != 1 else current_page_num
    next_page_num = current_page_num + 1 if current_page_num != page_counts else current_page_num

    # compute index_start and index_end of the list
    index_start = 1 if current_page_num == 1 else (current_page_num - 1) * int(num_each_page) + 1
    index_end = index_start + int(num_each_page) - 1
    index_end = index_end if index_end <= num_all else num_all

    return (last_page_num, next_page_num), (index_start, index_end)


def upload_file(file_project_dir, file_name, file_upload):
    """
    upload file
    :param file_project_dir:
    :param file_name:
    :param file_upload:
    :return:
    """
    file_dir = os.path.join(BASE_DIR, file_project_dir)
    if not os.path.exists(file_dir) or os.path.isfile(file_dir):
        mkdir_recursively(file_dir)
    file_full_path = os.path.join(file_dir, file_name)
    with open(file_full_path, 'wb+') as f:
        for chunk in file_upload.chunks():
            f.write(chunk)


def get_static_page(request, *args, **kwargs):
    url = request.path
    static_page_dir = getattr(settings, 'STATIC_PAGE_DIR')
    page_path = os.path.join(static_page_dir, url_to_path(url))
    try:
        # determine whether the stati page is useful, available
        assert os.path.exists(page_path)
        # assert the page is not modified
        print 'serving with static page...'
    except AssertionError:
        print 'No static page for this request, now generating...'
        # dev_env = getattr(settings, 'DEBUG', True)
        # if dev_env:
        #     print 'devlop env...'
        #     host = 'http://localhost:8000'
        # else:
        #     print 'product env...'
        #     host = 'http://localhost:80'
        ret = requests.get(request.build_absolute_uri())
        if ret.status_code == 200:
            with open(page_path, 'wb') as f:
                f.write(ret.text)
    try:
        with open(page_path) as f:
            return f.read(), True
    except:
        return '', False


def url_to_path(url):
    return url.strip('/')


class Descriptor(object):
    @staticmethod
    def ensure_authenticated(func):
        """
        :param func: 'request' must be the 1st parameter in args of func
        :return:
        """

        @wraps(func)
        def wrapper(*args, **kwargs):
            if not args[0].user.is_authenticated():
                return Http404
            res = func(*args, **kwargs)
            return res

        return wrapper


if __name__ == '__main__':
    get_static_page('/about')
