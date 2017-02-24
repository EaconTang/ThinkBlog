# coding=utf8
"""
爬虫获取多说动态评论，并发出邮件通知
"""
import sqlite3
import os
import time
import hashlib
import pprint
import json
import smtplib
import threading

import requests
from requests.exceptions import RequestException
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import WebDriverException, NoSuchElementException

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'db.sqlite3')
HOME_URL = "http://blog.tangyingkang.com"
PHANTOM_ADDR = "http://localhost:8910"
JSON_PATH = os.path.join(os.path.dirname(__file__), "comment.json")


def get_urls():
    """
    所有需要探测评论的url
    返回：[(url, title_content), ...],
    """

    URLS = [(HOME_URL + "/about/", "about_page"), ]
    sql_blog = """SELECT md_url, md_filename FROM blog_mdfile;"""
    sql_weibo = """SELECT wb_url, wb_text FROM blog_weibo;"""

    db = sqlite3.connect(DB_PATH)
    _cursor = db.cursor()

    # 博客URL
    _cursor.execute(sql_blog)
    res_blog = _cursor.fetchall()
    blog_url_format = HOME_URL + "/post/{}/"
    URLS += [(blog_url_format.format(url), title) for url, title in res_blog]

    # 微博URL
    _cursor.execute(sql_weibo)
    res_weibo = _cursor.fetchall()
    weibo_url_format = HOME_URL + "/weibo/{}/"
    URLS += [(weibo_url_format.format(url), title) for url, title in res_weibo]

    print "URLs counts: {}".format(len(URLS))
    return URLS


def fetch_comments(url, title=None):
    """
    获取评论

    如果有，返回{"url":, "title":, "count":, "top":, "detail": [{"user":, "content":, }, ...]}
    如果没有评论，返回{"url":, "title":, "count": 0, "top": 0, "detail": []}
    如果url不存在或者网络原因不可达，返回None
    :param url:
    :return:
    """
    broswer = webdriver.Remote(
        command_executor=PHANTOM_ADDR,
        desired_capabilities=DesiredCapabilities.PHANTOMJS
    )
    print "Fetching URL: {}".format(url)
    for _ in range(3):  # 重试3次
        try:
            broswer.get(url)
            if requests.get(url).status_code != 200:
                raise RequestException  # 网页出错
        except WebDriverException:
            if _ == 2:
                print "Fail to fetch url: {}".format(url)
                return None
            else:
                print "Cound not reach url({})! Wait 5 seconds and try again...".format(url)
                time.sleep(5)
                continue
        except RequestException:
            print "HTTP response code is not 200, ignoring URL: {}".format(url)
            return None

    # 默认等待10秒使多说加载完毕
    time.sleep(10)

    for _ in range(3):
        try:
            # 获取总评论数（多说js加载后提供的统计）
            total_comments = broswer.find_element_by_class_name("ds-comments-tab-duoshuo").text
            break
        except NoSuchElementException:
            # 多说还未完全加载
            if _ == 2:
                print "Give up this url: {}".format(url)
                return None
            else:
                print "Duoshuo is not loaded entirely! Wait 3 seconds and try again URL: {}".format(url)
                time.sleep(3)
                continue

    total_comments = int(str(total_comments).strip())
    if total_comments == 0:
        print "No comments! URL: {}".format(url)
        broswer.quit()
        return {"url": url, "title": title, "count": 0, "top": 0, "detail": []}

    detail_list = []  # 评论详情列表
    # 所有多说评论
    res = broswer.find_elements_by_class_name("ds-post-self")
    # 遍历获取用户名
    users = (_.find_element_by_class_name("ds-comment-header") for _ in res)
    # 遍历获取评论时间
    # times = (_.find_element_by_class_name("ds-time") for _ in res)
    # 遍历获取评论内容
    contents = (_.find_element_by_class_name("ds-comment-body").find_element_by_tag_name("p") for _ in res)
    # 置顶评论数
    top = len(res) - total_comments
    # 重设总评论数
    total_comments = len(res)

    for _user, _content in zip(users, contents):
        detail_list.append({
            "user": _user.text,
            # "datetime": _time.text,
            "content": _content.text
        })

    broswer.quit()
    _ret = {"url": url, "title": title, "count": total_comments, "top": top, "detail": detail_list}

    return _ret


def get_all_comments(urls):
    """
    获取所有URL的评论情况
    返回：{url_md5: {}, ...}
    """
    _url_comments = {}
    for url, title in urls:
        url_md5 = hashlib.new("md5", string=url).hexdigest()
        _comment = fetch_comments(url, title)
        if _comment is not None:
            _url_comments[url_md5] = _comment
    return _url_comments


class MyThread(threading.Thread):
    """带返回值的线程"""

    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)
        self._result = None

    def run(self):
        try:
            if self._Thread__target:  # __target这些是私有变量，需要添加前缀"_Thread"
                self._result = self._Thread__target(*self._Thread__args, **self._Thread__kwargs)
        finally:
            del self._Thread__target, self._Thread__args, self._Thread__kwargs

    @property
    def result(self):
        return self._result


def get_all_comments_concurrently(urls):
    """
    并发获取
    :param urls:
    :return:
    """
    threads = [MyThread(target=fetch_comments, args=(url, title)) for url, title in urls]
    for t in threads:
        t.setDaemon(True)
        t.start()
    for t in threads:
        t.join()
    res_list = [t.result for t in threads]

    _url_comments = {}
    for url_title, res in zip(urls, res_list):
        url, title = url_title
        if res is not None:
            url_md5 = hashlib.new("md5", string=url).hexdigest()
            _url_comments[url_md5] = res
    return _url_comments


def get_latest_comments():
    """
    获取最新的评论情况
    :return:
    """
    urls = get_urls()
    comments_latest = get_all_comments_concurrently(urls)
    return comments_latest


def get_last_comments():
    """
    获取上一次爬取的评论情况
    :return:
    """
    with open(JSON_PATH) as f:
        try:
            comments_last = json.load(f, encoding='utf-8')
        except ValueError:
            # ValueError: No JSON object could be decoded
            comments_last = {}
    return comments_last


def check_comments(_latest, _last):
    """
    比较最新评论和上一次评论详情
    :param _latest:
    :param _last:
    :return: 是否需要通知, 通知内容
    """
    notify_msg = []
    for url_md5 in _latest.keys():
        _notify, _msg = check_one(_latest[url_md5], _last.get(url_md5, None))
        if _notify:
            notify_msg.append(_msg)
    if notify_msg:
        return True, '\n'.join(notify_msg)
    else:

        return False, "No Change!"


def check_one(latest_comment, last_comment):
    """
    检查一个URL，最新评论和上一次评论变更情况
    :return: 是否需要通知, 通知内容
    """
    _url = latest_comment["url"]
    if last_comment is None:
        print "New URL: {}!".format(_url)
        last_comment = {}
    if latest_comment["detail"] == last_comment.get("detail", []):
        return False, "No change for URL: {}!".format(_url)
    print "Difference found for URL: {}! Last detail: {}; latest detail: {}".format(_url,
                                                                                    last_comment.get("detail", []),
                                                                                    latest_comment["detail"])
    if latest_comment["count"] > last_comment.get("count", 0):
        return True, 'New Comments! Click URL: {}'.format(_url)
    if latest_comment["count"] < last_comment.get("count", 0):
        return True, 'Comments deleted! Click URL: {}'.format(_url)
    if latest_comment["count"] == last_comment.get("count", 0):
        return True, 'Comments is updated! Click URL: {}'.format(_url)


def update_comments(_latest, _last):
    """保存评论"""
    print 'Update and Save comments to file: {}'.format(JSON_PATH)
    if not _last:
        _origin = {}
    else:
        _origin = _last
    _origin.update(_latest)
    with open(JSON_PATH, 'w') as f:
        json.dump(_origin, f, indent=2)


def send_notification(msg):
    """发送评论变更通知"""
    print msg


def sendmail(mail_to):
    """
    发送邮件通知
    :param mail_to:
    :return:
    """
    smtp = smtplib.SMTP("localhost", 25, local_hostname="eacon_aliyun")
    res = smtp.sendmail(
        from_addr='ds_notifier@eacon.ecs',
        to_addrs=[mail_to],
        msg="New comments!"
    )
    if not res:
        print "OK!"
    else:
        print res
    smtp.close()


def pretty_print(str):
    pprint.PrettyPrinter(indent=2).pprint(str)


def main():
    """"""
    _last = get_last_comments()
    _latest = get_latest_comments()
    _notify, _msg = check_comments(_latest=_latest, _last=_last)
    update_comments(_latest, _last)
    if _notify:
        send_notification(_msg)
    else:
        print _msg


if __name__ == '__main__':
    # print fetch_comments("http://blog.tangyingkang.com/post/2015/12/25/python-decorator/", 'python-decorator')
    main()
    # def foo(bar):
    #     return 'foo {}'.format(bar)
    #
    #
    # ts = [MyThread(target=foo, args=(i,)) for i in range(3)]
    # for t in ts:
    #     t.start()
    #
    # for t in ts:
    #     t.join()
    #
    # for t in ts:
    #     print t.result
