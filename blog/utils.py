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

def markdown_syntax():
    return """[Markdown Syntax]:
    标题

    文章内容较多时，可以用标题分段：
    
    标题1
    ======
    
    标题2
    -----
    
    ## 大标题 ##
    ### 小标题 ###
    粗斜体
    
    *斜体文本*    _斜体文本_
    **粗体文本**    __粗体文本__
    ***粗斜体文本***    ___粗斜体文本___
    链接
    
    常用链接方法
    
    文字链接 [链接名称](http://链接网址)
    网址链接 <http://链接网址>
    高级链接技巧
    
    这个链接用 1 作为网址变量 [Google][1].
    这个链接用 yahoo 作为网址变量 [Yahoo!][yahoo].
    然后在文档的结尾为变量赋值（网址）
    
      [1]: http://www.google.com/
      [yahoo]: http://www.yahoo.com/
    列表
    
    普通无序列表
    
    - 列表文本前使用 [减号+空格]
    + 列表文本前使用 [加号+空格]
    * 列表文本前使用 [星号+空格]
    普通有序列表
    
    1. 列表前使用 [数字+空格]
    2. 我们会自动帮你添加数字
    7. 不用担心数字不对，显示的时候我们会自动把这行的 7 纠正为 3
    列表嵌套
    
    1. 列出所有元素：
        - 无序列表元素 A
            1. 元素 A 的有序子列表
        - 前面加四个空格
    2. 列表里的多段换行：
        前面必须加四个空格，
        这样换行，整体的格式不会乱
    3. 列表里引用：
    
        > 前面空一行
        > 仍然需要在 >  前面加四个空格
    
    4. 列表里代码段：
    
        ```
        前面四个空格，之后按代码语法 ``` 书写
        ```
    
            或者直接空八个，引入代码块
    引用
    
    普通引用
    
    > 引用文本前使用 [大于号+空格]
    > 折行可以不加，新起一行都要加上哦
    引用里嵌套引用
    
    > 最外层引用
    > > 多一个 > 嵌套一层引用
    > > > 可以嵌套很多层
    引用里嵌套列表
    
    > - 这是引用里嵌套的一个列表
    > - 还可以有子列表
    >     * 子列表需要从 - 之后延后四个空格开始
    引用里嵌套代码块
    
    >     同样的，在前面加四个空格形成代码块
    >  
    > ```
    > 或者使用 ``` 形成代码块
    > ```
    图片
    
    跟链接的方法区别在于前面加了个感叹号 !，这样是不是觉得好记多了呢？
    
    ![图片名称](http://图片网址)
    当然，你也可以像网址那样对图片网址使用变量
    
    这个链接用 1 作为网址变量 [Google][1].
    然后在文档的结尾位变量赋值（网址）
    
     [1]: http://www.google.com/logo.png
    也可以使用 HTML 的图片语法来自定义图片的宽高大小
    
    <img src="htt://example.com/sample.png" width="400" height="100">
    换行
    
    如果另起一行，只需在当前行结尾加 2 个空格
    
    在当前行的结尾加 2 个空格  
    这行就会新起一行
    如果是要起一个新段落，只需要空出一行即可。
    
    分隔符
    
    如果你有写分割线的习惯，可以新起一行输入三个减号-。当前后都有段落时，请空出一行：
    
    前面的段落
    
    ---
    
    后面的段落
    
    高级技巧
    行内 HTML 元素
    
    目前只支持部分段内 HTML 元素效果，包括 <kdb> <b> <i> <em> <sup> <sub> <br> ，如
    
    键位显示
    
    使用 <kbd>Ctrl<kbd>+<kbd>Alt<kbd>+<kbd>Del<kbd> 重启电脑
    代码块
    
    使用 <pre></pre> 元素同样可以形成代码块
    粗斜体
    
    <b> Markdown 在此处同样适用，如 *加粗* </b>
    符号转义
    
    如果你的描述中需要用到 markdown 的符号，比如 _ # * 等，但又不想它被转义，这时候可以在这些符号前加反斜杠，如 \_ \# \* 进行避免。
    
    \_不想这里的文本变斜体\_
    \*\*不想这里的文本被加粗\*\*
    """

