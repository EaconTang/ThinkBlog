# coding=utf-8
from django.http import HttpResponse
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
    _all = MDFile.objects.all()
    res = '<ul>\n'
    for each in _all:
        # res += ''.join(['<li>', each.md_filename, '(Visit: ', str(each.md_visit), ') </li>\n'])
        file_with_url = '<a href="{}">{}</a>'.format(each.md_url, each.md_filename)
        res += '<li> {} (visit: {}) </li>\n'.format(file_with_url, each.md_visit)
    res += '</ul>'
    return HttpResponse(res)

def get_by_name(request, filename):
    md_text = MDFile.objects.get(md_filename=filename).md_text
    return MDResponse(md_text=md_text)

def get_by_url(request, url):
    md_text = MDFile.objects.get(md_url=url).md_text
    return MDResponse(md_text=md_text)
