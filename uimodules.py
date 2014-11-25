import tornado.web
from Worker import Worker

class docModule(tornado.web.UIModule):
    def render(self,doc):
        return self.render_string('modules/document.html',doc = doc)

class showdocModule(tornado.web.UIModule):
    def render(self,doc):
    	self.doc = doc
        return self.render_string('modules/showdocument.html',doc = doc)