# coding=utf-8

import os
from tornado.web import Application,RedirectHandler
from tornado.ioloop import IOLoop
from handlers.ChatHandler import ChatHandler
from handlers.ChatWHandler import ChatWHandler
from tornado.options import parse_command_line,define, options

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

define("address", default='0.0.0.0', help="监听地址", type=str)
define("port", default=8888, help="监听端口", type=str)

if __name__ == '__main__':
    parse_command_line()
    MainApplication().listen(options.port, address=options.address)
    IOLoop.instance().start()





