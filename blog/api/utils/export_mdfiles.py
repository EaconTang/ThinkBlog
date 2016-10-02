# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import os
import sqlite3
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
mdfiles_dir = os.path.join(base_dir, 'mdfile')
if not os.path.exists(mdfiles_dir):
    os.mkdir(mdfiles_dir)


def select_db():
    SQL = """select * from blog_mdfile;"""
    conn = sqlite3.connect(os.path.join(base_dir, 'db.sqlite3'))
    cur = conn.cursor()
    cur.execute(SQL)
    return cur.fetchall()


def gen_path(url, publish_time, file_title):
    if publish_time:
        year, month, day = publish_time.split(' ')[0].split('-')
    else:
        raise Exception('time puzzle for {}?'.format(file_title))

    if not os.path.exists(os.path.join(mdfiles_dir, year, month, day)):
        if not os.path.exists(os.path.join(mdfiles_dir, year, month)):
            if not os.path.exists(os.path.join(mdfiles_dir, year)):
                os.mkdir(os.path.join(mdfiles_dir, year))
            os.mkdir(os.path.join(mdfiles_dir, year, month))
        os.mkdir(os.path.join(mdfiles_dir, year, month, day))

    return os.path.join(mdfiles_dir, year, month, day, file_title)


def main():
    for each in select_db():
        md_text = each[3]
        md_info = {
            'url': each[1].strip(),
            'file_title': each[2].strip(),
            'publish_time': each[4].__str__(),
            'visit': each[7].__str__(),
            # 'categories': mdfile.categories,
            # 'tags': mdfile.tags,
            'summary': each[8],
            'is_draft': each[9].__str__(),
        }
        file_path = gen_path(md_info['url'], md_info['publish_time'], md_info['file_title'])
        print "exporting: ", file_path
        with open('.'.join([file_path, 'md']), 'w') as f:
            json.dumps(md_info, indent=4, ensure_ascii=False)
            f.write(md_text)
        with open('.'.join([file_path, 'meta']), 'w') as f:
            f.write(json.dumps(md_info, indent=4, ensure_ascii=False))
        print 'export success: {}'.format(md_info['file_title'])


if __name__ == '__main__':
    main()
