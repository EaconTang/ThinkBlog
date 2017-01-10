# MyBlog

### 部署事项
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
