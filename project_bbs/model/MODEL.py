#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pymysql


class CreateCookie(object):

    def cookie(self):   # 返回一个随机字符串作为cookie
        import time
        import hashlib
        t = time.time()
        h = hashlib.md5()
        h.update(bytes(str(t), encoding='utf-8'))
        ret = h.hexdigest()
        return ret


class ChangeInfoUser(object):

    def __init__(self):     # 初始化函数，建立与数据库project_bbs的链接
        self.conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='project_bbs')
        self.cursor = self.conn.cursor()

    def add_info(self, user_name, user_pwd):  # 添加用户名和密码到info_user表中
        self.cursor.executemany("insert into info_user (user_name,user_pwd) values (%s,%s)", [(user_name, user_pwd)])
        self.conn_finish()

    def del_info(self, user_name):  # 输入用户名，把用户名从info_user表中删除
        self.cursor.executemany("delete from info_user where user_name=%s", [user_name])
        self.conn_finish()

    def search_info(self, user_name):  # 输入用户名，如果用户名存在info_user表中则返回用户名和密码，如果不在表中则返回none
        self.cursor.executemany("select user_name,user_pwd from info_user where user_name=%s", [user_name])
        ret = self.cursor.fetchone()
        self.conn_finish()
        return ret

    def return_user_name(self, user_id):
        self.cursor.executemany("select user_name from info_user where user_id=%s", [user_id])
        ret = self.cursor.fetchone()
        return ret[0]

    def update_info(self, user_name, user_pwd):  # 输入用户名和新密码密码，把info_user表中对应的用户名的密码改为新密码
        self.cursor.executemany("update info_user set user_pwd=%s where user_name=%s", [(user_pwd, user_name)])
        self.conn_finish()

    def conn_finish(self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()


class ChangeInfoNews(object):

    def __init__(self):     # 初始化函数，建立与数据库project_bbs的链接
        self.conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='',
                                    db='project_bbs', charset='utf8')
        self.cursor = self.conn.cursor()

    def add_info(self, title, news_type, user_id, content):  # 添加帖子标题，类型，发布人，内容到info_user表中
        self.cursor.executemany("insert into info_news (title,type,publisher,content) values (%s,%s,%s,%s)",
                                [(title, news_type, user_id, content)])
        self.conn_finish()

    def del_info(self, news_title):     # 输入帖子标题删除数据库中的帖子
        self.cursor.executemany("delete from info_news where title=%s", [news_title])
        self.conn_finish()

    def search_info(self, news_type):     # 输入参数——quanbu,xinwen,duanzi,keji,youxi
                                            # 返回该类型帖子标题，发布人，时间，类型，内容，点赞数的列表
        if news_type == 'xinwen':
            news_type = '新闻'
        elif news_type == 'duanzi':
            news_type = '段子'
        elif news_type == 'keji':
            news_type = '科技'
        elif news_type == 'youxi':
            news_type = '游戏'
        else:
            news_type = '%'
        self.cursor.executemany("select A.title,A.user_name,A.time,A.type,A.content,B.likes from \
        (select info_news.title,info_user.user_name,info_news.time,info_news.type,info_news.content,info_news.news_id \
        from info_news,info_user where info_news.publisher=info_user.user_id) as A left join \
        (select  news_id,count(user_id) as likes from info_like group by news_id) as B on A.news_id = B.news_id \
        where A.type like %s;", [news_type])
        ret = self.cursor.fetchall()
        self.conn_finish()
        li_news = []
        for i in ret:
            ii = list(i)
            ii[2] = ii[2].strftime("%Y-%m-%d %H:%M")
            if not ii[5]:
                ii[5] = 0
            li_news.append(ii)
        return li_news

    def conn_finish(self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()


class ChangeInfoCookie(object):

    def __init__(self):     # 初始化函数，建立与数据库project_bbs的链接
        self.conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='',
                                    db='project_bbs', charset='utf8')
        self.cursor = self.conn.cursor()

    def add_info(self, user_name, cookie):    # 添加user_name和对应的cookie到数据库中
        self.cursor.executemany("insert into info_cookie (user_id,cookie) values ((select user_id from info_user \
        where user_name = %s),%s)", [(user_name, cookie)])
        self.conn_finish()

    def search_info(self, cookie):      # 输入cookie,如果输入的cookie存在于数据库则返回user_id,不存在返回none
        self.cursor.executemany("select user_id from info_cookie where cookie = %s", [cookie])
        ret = self.cursor.fetchone()
        self.conn_finish()
        if ret == None:
            return none
        else:
            ret = str(ret[0])
            return ret

    def conn_finish(self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()


class ChangeInfoLike(object):

    def __init__(self):     # 初始化函数，建立与数据库project_bbs的链接
        self.conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='',
                                    db='project_bbs', charset='utf8')
        self.cursor = self.conn.cursor()

    def add_info(self, user_id, title):     # 添加user_id和帖子序号到点赞数据库，如果存在返回False
        try:
            self.cursor.executemany("insert into info_like (news_id,user_id) values \
                        ((select news_id from info_news where title=%s),%s)", [(title, user_id)])
            self.conn_finish()
            return True
        except:
            return False

    def search_info(self, news_id):
        self.cursor.executemany('select user_id from info_like where news_id=%s', [news_id])
        ret = self.cursor.fetchall()
        ret = list(ret)
        return ret

    def conn_finish(self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()



