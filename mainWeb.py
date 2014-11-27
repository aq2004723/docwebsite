#coding=utf-8

import os.path

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from Worker import Worker
import time 
import uimodules


from tornado.options import define, options
define("port", default=8093, help="run on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self):
        self.db = Worker()
        template_path=os.path.join(os.path.dirname(__file__), "templates")
        static_path=os.path.join(os.path.dirname(__file__), "static")
        settings = {
            'cookie_secret': "CkwXIkG6RCa48skVeMBhdbJKt0QSqk1tivD1smsr98Y=",
            'login_url': "/login",
            'template_path':template_path,
            'static_path':static_path,
            'ui_modules':uimodules,
        }

       

        handlers=[(r'/', IndexHandler), 
            (r'/login', LoginHandler), 
            (r'/logout', LogoutHandler), 
            (r'/doc/(\d+)',DocviewHandler),
            (r'/upload',UseruploadHandler),
            (r'/user',UserInfoHandler),
        ]
        tornado.web.Application.__init__(self, handlers, **settings)


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self): 
        return self.get_secure_cookie("username")

class LoginHandler(BaseHandler):
    @tornado.web.asynchronous
    def post(self):
        username = self.get_argument("username")
        password = self.get_argument("password")
        result = self.application.db.signin(username,password)
        if result is not None:
            self.set_secure_cookie("username", username)
            self.finish('0')
        else:   
            self.finish('-1')

class IndexHandler(BaseHandler):
    def get(self):
        docs = list(self.application.db.getIndexDoc())
        self.render('index.html',user=self.current_user,docs = docs)


class LogoutHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.clear_cookie("username")
        self.redirect('/')

class UserInfoHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        userinfo = self.application.db.getuserinfo(self.current_user)
        userDocs = list(self.application.db.getuserUpload(self.current_user) )
        self.render('userinfo.html',user=self.current_user, userinfo=userinfo,userDocs=userDocs)

class DocviewHandler(BaseHandler):
    def get(self,docID):
        rs = self.application.db.getDoc(docID)
        self.render('viewer.html',rs = rs)

class UseruploadHandler(BaseHandler):
    def post(self):
        docname=self.get_argument('docname')
        description=self.get_argument('docdetail')
        myfile = self.request.files['docfile'][0]
        result = self.application.db.userupload(docname,description,myfile,"",self.current_user)
        self.redirect("/user")

class SearchHandler(BaseHandler):
    def post(self):
        docs = self.application.db.search_doc(self.get_argument('keywords'))
        self.render('result.html',user=current_user,docs = docs)

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = Application()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()