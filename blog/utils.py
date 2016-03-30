# coding=utf-8
"""
"""
from django.shortcuts import HttpResponse, render_to_response
import markdown


def html_response(*args, **kwargs):
    return render_to_response(*args, **kwargs)


def exist_html(filename):
    # To do
    return False

class MDResponse(HttpResponse):
    def __init__(self, md_text='', *args, **kwargs):
        super(HttpResponse, self).__init__(*args, **kwargs)
        # file_path = os.path.join("source", '.'.join([filename, "md"]))
        # try:
        #     with open(file_path) as f:
        #         self.content = markdown.markdown(f.read())
        # except (IOError, FileNotFoundError) as e:
        #     self.content = "Error!"
        # finally:
        #     pass
        self.content = MarkdownRender(md_text).html


class MarkdownRender(object):
    def __init__(self, text):
        self._html = markdown.markdown(text)

    @property
    def html(self):
        return self._html


class MyResponse(object):
    def __init__(self):
        pass

