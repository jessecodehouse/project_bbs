#!/usr/bin/env python
# -*- coding:utf-8 -*-

import tornado.web
import tornado.ioloop
from controller import REGISTER_LOGIN
from model import MODEL


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        db_info_news = MODEL.ChangeInfoNews()
        li_news = db_info_news.search_info('')
        self.render('index.html', li_news=li_news)


class Xinwen(tornado.web.RequestHandler):

    def get(self):
        db_info_news = MODEL.ChangeInfoNews()
        li_news = db_info_news.search_info('xinwen')
        self.render('xinwen.html', li_news=li_news)


class Duanzi(tornado.web.RequestHandler):
    def get(self):
        db_info_news = MODEL.ChangeInfoNews()
        li_news = db_info_news.search_info('duanzi')
        self.render('duanzi.html', li_news=li_news)


class Youxi(tornado.web.RequestHandler):
    def get(self):
        db_info_news = MODEL.ChangeInfoNews()
        li_news = db_info_news.search_info('youxi')
        self.render('youxi.html', li_news=li_news)


class Keji(tornado.web.RequestHandler):
    def get(self):
        db_info_news = MODEL.ChangeInfoNews()
        li_news = db_info_news.search_info('keji')
        self.render('keji.html', li_news=li_news)


class Register(tornado.web.RequestHandler):

    def post(self, *args, **kwargs):
        user_name = self.get_argument('register_user_name')
        rl = REGISTER_LOGIN.RegisterAndLogin()
        if rl.test_user_name_exist(user_name):  # 判断用户名是否存在于数据库中，存在返回True
            self.write('exist')
        else:
            user_pwd = self.get_argument('register_pwd')
            db = MODEL.ChangeInfoUser()
            db.add_info(user_name, user_pwd)    # 把用户名和密码添加到数据库中
            self.write('success')


class Login(tornado.web.RequestHandler):

    def post(self, *args, **kwargs):

        user_name = self.get_argument('login_user_name')
        pwd = self.get_argument('login_pwd')
        rl = REGISTER_LOGIN.RegisterAndLogin()
        if rl.test_user_name_and_pwd(user_name, pwd):    # 输入用户名和密码判断是否和数据库一致
            c = self.get_cookie('bbs')
            db_info_cookie = MODEL.ChangeInfoCookie()
            if c:
                f = db_info_cookie.search_info(c)
                if f:
                    print(f)
                else:
                    db_info_cookie = MODEL.ChangeInfoCookie()
                    new_c = MODEL.CreateCookie()
                    new_cookie = new_c.cookie()
                    self.set_cookie('bbs', new_cookie, expires_days=60)
                    db_info_cookie.add_info(user_name, new_cookie)
            else:
                new_c = MODEL.CreateCookie()
                new_cookie = new_c.cookie()
                self.set_cookie('bbs', new_cookie, expires_day=60)
                db_info_cookie.add_info(user_name, new_cookie)
            self.write('success')
        else:
            self.write('error')


class Publish(tornado.web.RequestHandler):

    def post(self, *args, **kwargs):
        title = self.get_argument('title')
        news_type = self.get_argument('news_type')
        content = self.get_argument('content')
        c = self.get_cookie('bbs')
        db_info_cookie = MODEL.ChangeInfoCookie()
        user_id = db_info_cookie.search_info(c)
        db_info_news2 = MODEL.ChangeInfoNews()
        db_info_news2.add_info(title, news_type, user_id, content)
        self.write('success')


class Like(tornado.web.RequestHandler):

    def post(self, *args, **kwargs):
        c = self.get_cookie('bbs')
        db_info_cookie = MODEL.ChangeInfoCookie()
        user_id = db_info_cookie.search_info(c)
        title = self.get_argument('title')
        db_info_like = MODEL.ChangeInfoLike()
        if db_info_like.add_info(user_id, title):
            self.write('success')
        else:
            self.write('error')



settings = {
    'template_path': 'tpl',
    'static_path': 'statics',
    'static_url_prefix': '/statics/',
}

application = tornado.web.Application([
    (r'/index', MainHandler),
    (r'/youxi', Youxi),
    (r'/xinwen', Xinwen),
    (r'/duanzi', Duanzi),
    (r'/keji', Keji),
    (r'/register', Register),
    (r'/login', Login),
    (r'/publish', Publish),
    (r'/like', Like),
], **settings)

if __name__ == '__main__':
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
