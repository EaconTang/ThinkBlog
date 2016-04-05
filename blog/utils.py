# coding=utf-8
"""
"""
from django.shortcuts import HttpResponse, render_to_response
import markdown2, markdown


def html_response(*args, **kwargs):
    return render_to_response(*args, **kwargs)


def exist_html(filename):
    # To do
    return False

class MDResponse(HttpResponse):
    def __init__(self, md_text='', *args, **kwargs):
        super(HttpResponse, self).__init__(*args, **kwargs)
        self.content = MarkdownRender(md_text).html


class MarkdownRender(object):
    def __init__(self, text):
        # self._html = markdown2.markdown(text)
        self._html = markdown.markdown(text)

    @property
    def html(self):
        return self._html


class MyResponse(object):
    def __init__(self):
        pass


def markdown_syntax():
    return """
    Markdown语法说明: http://www.jianshu.com/p/q81RER
    """
