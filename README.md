# ThinkBlog

ThinkBlog是基于Django开发的简洁博客网站，实现了博客网站的各种常用功能：
- markdown语法编写博客
- 博客归档
- 多分类、多标签建模
- 增加微博实现
- pygments代码高亮
- 简单易用的文件管理界面，方便上传和加载静态资源
- 自动定时备份
- 集成七牛cdn加速
- ~~集成多说评论~~
    - ~~基于PhantomJS(Docker)爬取动态js实现自定义的评论信息检测，并通过邮件通知~~
    - 多说评论要倒闭了，换搜狐畅言
- ECharts访问统计图表
- 基于Celery实现后台任务队列
- 使用uwsgi+supervisord启动和管理进程


## 部署手记
- [可选]virtualenv
- pip install -r requirements.txt
- 数据库初始化
    + python manage.py makemigrations
    + python manage.py migrate
- collectstatic收集静态文件
    + python manage.py collectstatic
- Settings文件设置:
    - DEBUG=False
    - ALLOWED_HOSTS
    - STATIC_URL
        - 服务器本地: /static/
        - 七牛：替换七牛cdn
    - URL_PREFIX
    - BLOG_EACH_PAGE
-  uWSGI
    +  uwsgi --ini uwsgi_blog.ini
-  Nginx
    - 注意防蚊权限(数据库等)
- ~~docker-phantomJS~~
    - ~~ ```docker run -d --name phantomJS -p 8910:8910 -v /etc/localtime:/etc/localtime wernight/phantomjs phantomjs --webdriver=8910``` ~~
- 启动Reids
    - ```docker run -d --name redis --restart=always -p 6379:6379 redis```
- 启动Celery Worker
    - ```celery worker -A ThinkBlog --loglevel info --logfile /opt/ThinkBlog/logs/celery_worker.log```
- 使用supervisord启动
    - ```echo_supervisord_conf > /etc/supervisord.conf```
    - ```cat ThinkBlog/supervisord.conf >> /etc/supervisord.conf```
    - ```supervisord -c /etc/supervisord.conf```


## 依赖
- 数据库：
    - sqlite3
    - redis