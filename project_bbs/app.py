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
        db_info_news = MODEL.ChangeInfoNews()
        hot_news = db_info_news.search_hot_info()
        c = self.get_cookie('bbs')
        if not c:
            flag_r_l = 'show'
            flag_user_name = 'none'
            user_name = ''
        else:
            db_info_cookie = MODEL.ChangeInfoCookie()
            user_name = db_info_cookie.search_user_name(c)
            if not user_name:
                flag_r_l = 'show'
                flag_user_name = 'none'
            else:
                flag_r_l = 'none'
                flag_user_name = 'show'
        self.render('index.html', li_news=li_news, hot_news=hot_news,
                    flag_r_l=flag_r_l, flag_user_name=flag_user_name, user_name=user_name)


class Xinwen(tornado.web.RequestHandler):

    def get(self):
        db_info_news = MODEL.ChangeInfoNews()
        li_news = db_info_news.search_info('xinwen')
        db_info_news = MODEL.ChangeInfoNews()
        hot_news = db_info_news.search_hot_info()
        c = self.get_cookie('bbs')
        if not c:
            flag_r_l = 'show'
            flag_user_name = 'none'
            user_name = ''
        else:
            db_info_cookie = MODEL.ChangeInfoCookie()
            user_name = db_info_cookie.search_user_name(c)
            if not user_name:
                flag_r_l = 'show'
                flag_user_name = 'none'
            else:
                flag_r_l = 'none'
                flag_user_name = 'show'
        self.render('xinwen.html', li_news=li_news, hot_news=hot_news,
                    flag_r_l=flag_r_l, flag_user_name=flag_user_name, user_name=user_name)


class Duanzi(tornado.web.RequestHandler):
    def get(self):
        db_info_news = MODEL.ChangeInfoNews()
        li_news = db_info_news.search_info('duanzi')
        db_info_news = MODEL.ChangeInfoNews()
        hot_news = db_info_news.search_hot_info()
        c = self.get_cookie('bbs')
        if not c:
            flag_r_l = 'show'
            flag_user_name = 'none'
            user_name = ''
        else:
            db_info_cookie = MODEL.ChangeInfoCookie()
            user_name = db_info_cookie.search_user_name(c)
            if not user_name:
                flag_r_l = 'show'
                flag_user_name = 'none'
            else:
                flag_r_l = 'none'
                flag_user_name = 'show'
        self.render('duanzi.html', li_news=li_news, hot_news=hot_news,
                    flag_r_l=flag_r_l, flag_user_name=flag_user_name, user_name=user_name)


class Youxi(tornado.web.RequestHandler):
    def get(self):
        db_info_news = MODEL.ChangeInfoNews()
        li_news = db_info_news.search_info('youxi')
        db_info_news = MODEL.ChangeInfoNews()
        hot_news = db_info_news.search_hot_info()
        c = self.get_cookie('bbs')
        if not c:
            flag_r_l = 'show'
            flag_user_name = 'none'
            user_name = ''
        else:
            db_info_cookie = MODEL.ChangeInfoCookie()
            user_name = db_info_cookie.search_user_name(c)
            if not user_name:
                flag_r_l = 'show'
                flag_user_name = 'none'
            else:
                flag_r_l = 'none'
                flag_user_name = 'show'
        self.render('youxi.html', li_news=li_news, hot_news=hot_news,
                    flag_r_l=flag_r_l, flag_user_name=flag_user_name, user_name=user_name)


class Keji(tornado.web.RequestHandler):
    def get(self):
        db_info_news = MODEL.ChangeInfoNews()
        li_news = db_info_news.search_info('keji')
        db_info_news = MODEL.ChangeInfoNews()
        hot_news = db_info_news.search_hot_info()
        c = self.get_cookie('bbs')
        if not c:
            flag_r_l = 'show'
            flag_user_name = 'none'
            user_name = ''
        else:
            db_info_cookie = MODEL.ChangeInfoCookie()
            user_name = db_info_cookie.search_user_name(c)
            if not user_name:
                flag_r_l = 'show'
                flag_user_name = 'none'
            else:
                flag_r_l = 'none'
                flag_user_name = 'show'
        self.render('keji.html', li_news=li_news, hot_news=hot_news,
                    flag_r_l=flag_r_l, flag_user_name=flag_user_name, user_name=user_name)


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
            c = MODEL.CreateCookie()
            new_c = c.cookie()
            db_cookie = MODEL.ChangeInfoCookie()
            db_cookie.add_info(user_name, new_c)
            self.write('success')


class Login(tornado.web.RequestHandler):

    def post(self, *args, **kwargs):
        user_name = self.get_argument('login_user_name')
        pwd = self.get_argument('login_pwd')
        rl = REGISTER_LOGIN.RegisterAndLogin()
        ret = rl.test_user_name_and_pwd(user_name, pwd)    # 输入用户名和密码判断是否和数据库一致
        if ret:
            db_info_cookie = MODEL.ChangeInfoCookie()
            exist_c = db_info_cookie.search_cookie(user_name)
            self.set_cookie('bbs', exist_c, expires_days=None)
            self.write('success')
        else:
            self.write('error')


class Publish(tornado.web.RequestHandler):

    def post(self, *args, **kwargs):
        c = self.get_cookie('bbs')
        db_info_cookie = MODEL.ChangeInfoCookie()
        user_id = db_info_cookie.search_info(c)
        if not user_id:
            self.write('nocookie')
        else:
            title = self.get_argument('title')
            news_type = self.get_argument('news_type')
            content = self.get_argument('content')
            db_info_news2 = MODEL.ChangeInfoNews()
            db_info_news2.add_info(title, news_type, user_id, content)
            self.write('success')


class Like(tornado.web.RequestHandler):

    def post(self, *args, **kwargs):
        c = self.get_cookie('bbs')
        db_info_cookie = MODEL.ChangeInfoCookie()
        user_id = db_info_cookie.search_info(c)
        if not user_id:
            self.write('nocookie')
        else:
            news_id = self.get_argument('title')
            db_info_like = MODEL.ChangeInfoLike()
            if db_info_like.add_info(user_id, news_id):
                self.write('success')
            else:
                self.write('error')


class New(tornado.web.RequestHandler):

    def get(self, news_id):
        db_info_news = MODEL.ChangeInfoNews()
        one_new = db_info_news.search_one_new(news_id)
        self.render('one_new.html', one_new=one_new)


settings = {
    'template_path': 'tpl',
    'static_path': 'statics',
    'static_url_prefix': '/statics/',
}

application = tornado.web.Application([
    (r'/', MainHandler),
    (r'/youxi', Youxi),
    (r'/xinwen', Xinwen),
    (r'/duanzi', Duanzi),
    (r'/keji', Keji),
    (r'/register', Register),
    (r'/login', Login),
    (r'/publish', Publish),
    (r'/like', Like),
    (r'/(\d*)', New)
], **settings)

if __name__ == '__main__':
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
