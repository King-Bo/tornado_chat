# coding=utf-8

from tornado.web import RequestHandler

class ChatHandler(RequestHandler):
    def get(self):
        self.write('123')
