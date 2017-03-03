# coding=utf-8

import json
from datetime import datetime
from tornado.websocket import WebSocketHandler

# 最大房间数100，每个房间最大用户数100
MAX_ROOMS = 100
MAX_USERS_PER_ROOM = 100

class ChatWHandler(WebSocketHandler):

    # 房间信息字典,初始化房间1，2，3，4
    rooms = {'1':[],'2':[],'3':[],'4':[]}
    # websocket连接关联用户名和房间信息字典
    wsconns = {}

    def open(self):
        self.wsconns[self] = {'room': None,'user_id': 'god'}

    # 根据前端发送的不同指令，执行不同函数
    def on_message(self, message):
        data = json.loads(message)
        print(data)
        user_id = data.get('user_id','')
        room_id = data.get('room_id','')
        message = data.get('message','')

        if data['action'] == 'change_user_id':
            result = self.change_user_id(user_id)
            if result['status'] == 'ok':
                self.update_all_page()
            else:
                self.write_message(result)
        elif data['action'] == 'new_room':
            result = self.new_room(room_id)
            if result['status'] == 'ok':
                self.update_all_page()
            else:
                self.write_message(result)
        elif data['action'] == 'enter_room':
            result = self.enter_room(room_id)
            if result['status'] == 'ok':
                self.update_all_page()
            else:
                self.write_message(result)
        elif data['action'] == 'send_message':
            self.write_message(self.send_message(message))

    # 更换用户名
    def change_user_id(self, user_id):
        self.wsconns[self]['user_id'] = user_id
        return {'status': 'ok'}

    # 新建房间
    def new_room(self, room_id):
        if room_id in self.rooms:
            return {'status': '房间名已存在'}
        elif len(self.rooms) >= 100:
            return {'status': '达到最大房间数'}
        else:
            self.rooms[room_id] = []
            return {'status': 'ok'}

    # 当前用户加入房间
    def enter_room(self, room_id):
        try:
            pre_room_id = self.wsconns[self]['room']
            if len(self.rooms[room_id]) >= 100:
                return {'status': '该房间已满'}

            # 把该用户移出之前房间
            if pre_room_id:
                self.rooms[pre_room_id].remove(self)
                # 如果前房间没有用户了，删除前房间
                #if not self.rooms[pre_room_id]:
                    #del self.rooms[pre_room_id]

            # 把该用户加入现房间
            self.wsconns[self]['room'] = room_id
            self.rooms[room_id].append(self)
            return {'status': 'ok'}
        except Exception as e:
            return {'status': '房间名不存在'}

    # 给当前房间其他用户发送消息
    def send_message(self, message):
        try:
            room = self.wsconns[self]['room']
            for wsconn in self.rooms[room]:
                wsconn.write_message({'user': self.wsconns[self]['user_id'],
                                      'message': message,
                                      'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
            return {'status': 'ok'}
        except Exception as e:
            print(e)
            return {'status': '房间名不存在'}

    # 给所有用户推送最新的房间信息和用户所在房间的用户信息
    def update_all_page(self):
        for wsconn in self.wsconns:
            room = self.wsconns[wsconn]['room']
            if room:
                wsconn.write_message({'rooms': sorted(self.rooms.keys()),
                                      'users': [self.wsconns[i]['user_id'] for i in self.rooms[room]]})

    # websocket关闭时删除用户并退出房间
    def delete_user(self):
        room = self.wsconns[self]['room']
        if room in self.rooms:
            self.rooms[room].remove(self)
        if self in self.wsconns:
            del self.wsconns[self]
        self.update_all_page()

    def on_close(self):
        self.delete_user()




