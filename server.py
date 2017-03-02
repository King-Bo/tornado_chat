# coding=utf-8

import os
from tornado.web import Application,RedirectHandler
from tornado.ioloop import IOLoop
from handlers.ChatHandler import ChatHandler
from handlers.ChatWHandler import ChatWHandler

class MainApplication(Application):
    def __init__(self):
        settings = {
            'template_path': os.path.join((os.path.dirname(__file__)),'template'),
            'static_path': os.path.join((os.path.dirname(__file__)),'static'),
            'debug': True
        }
        handlers = [
            (r'/', RedirectHandler, {"url": "/chat"}),
            (r'/chat', ChatHandler),
            (r'/chat_soc', ChatWHandler),
        ]
        super(MainApplication,self).__init__(handlers=handlers,**settings)

if __name__ == '__main__':
    MainApplication().listen(80)
    IOLoop.instance().start()





