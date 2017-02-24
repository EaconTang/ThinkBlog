# MyBlog

## 基于Django的个人博客
- 实现了博客网站的各种常用功能
    - markdown语法编写博客
    - 博客归档
    - 多分类、多标签建模
    - 增加微博实现
    - pygments代码高亮
    - 集成多说评论
    - 集成七牛cdn加速
    - 简单易用的文件管理界面，方便上传和加载静态资源
    - 自动定时备份
    - 基于PhantomJS(Docker)爬取动态js实现自定义的评论信息检测，并通过邮件通知


## 部署手记
- [可选]virtualenv
- pip install -r requirements.txt
- 数据库初始化
    + python manage.py makemigrations
    + python manage.py migrate
- collectstatic收集静态文件
- Settings文件设置:
    - DEBUG=False
    - ALLOWED_HOSTS
    - STATIC_URL
        - 服务器本地: /static/
        - 七牛
    - URL_PREFIX
    - BLOG_EACH_PAGE
-  uWSGI
    +  uwsgi --ini uwsgi_blog.ini
-  Nginx
    - 注意防蚊权限(数据库等)
