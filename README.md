# MyBlog

### 部署事项
- [可选]virtualenv
- pip install -r requirements.txt
- 数据导入
- collectstatic静态文件
- Settings文件设置:
    - DEBUG=False
    - ALLOWED_HOSTS
    - STATIC_URL
        - 服务器本地: /static/
        - 七牛
    - URL_PREFIX
    - BLOG_EACH_PAGE
-  uWSGI
-  Nginx
    - 权限(数据库等)
