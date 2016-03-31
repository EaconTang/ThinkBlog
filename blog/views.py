# coding=utf-8
# from __future__ import unicode_literals
import os
from django.http import HttpResponse
from django.shortcuts import render_to_response
from MyBlog.settings import BASE_DIR
import markdown
from .utils import MDResponse
from .models import MDFile

# Create your views here.
# def index(request):
#     # with open("index.md") as f:
#         # return HttpResponse(content=markdown.markdown(f.read()))
#     return MDResponse(filename="index")
#
# def cmd_markdown(request):
#     return MDResponse(filename="cmd-markdown")
#
# def test(request):
#     return MDResponse(filename="test")

def home(request):
    blog_list = MDFile.objects.all()
    # res = '<ul>\n'
    # for each in _all:
    #     # res += ''.join(['<li>', each.md_filename, '(Visit: ', str(each.md_visit), ') </li>\n'])
    #     file_with_url = '<a href="{}">{}</a>'.format(each.md_url, each.md_filename)
    #     res += '<li> {} (visit: {}) </li>\n'.format(file_with_url, each.md_visit)
    # res += '</ul>'
    # return HttpResponse(res)
    context = {}
    # blog_list = []
    # for each in _all:
    #     blog_list.append('<a href="{}">{}</a>'.format(each.md_url, each.md_filename))
    context = {
        'blog_list': blog_list,
    }
    return render_to_response("home.html", context)




def get_by_name(request, filename):
    md_text = MDFile.objects.get(md_filename=filename).md_text
    return MDResponse(md_text=md_text)


def get_by_url(request, url):
    md_object = MDFile.objects.get(md_url=url)
    md_text = md_object.md_text
    # return MDResponse(md_text=md_text)
    article_body = markdown.markdown(md_text)
    context = {
        'article_html': article_body,
        "article_md_text": md_text,
        'article_md_object': md_object
    }
    # return render_to_response("article.html", context)
    # with open(os.path.join(BASE_DIR, "blog/templates/article.html")) as f:
    #     html = f.read().decode(encoding="utf-8")
    # html.replace("{{ article_body }}", article_body)
    # return HttpResponse(content=b"{}".format(html),)

    return render_to_response("article.html", context)
