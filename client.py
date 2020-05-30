# -*- coding: utf-8 -*-
"""
主要功能是连接服务器，以及向消息队列添加消息
"""
import json
import os
import queue
import socket
import time

from clientthread import ClientThread
from resource import msgtype


class Client:
    def __init__(self, host, port):
        self.msg = ''
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.outputs = []  # 流出
        self.inputs = []  # 流入
        self.send_msg_queue = queue.Queue()  # 待发送的消息的队列
        self.msg = ''
        self.userList = []  # 在线用户名列表
        self.name = ''

    # 连接服务器
    def connect(self):
        self.sock.connect((self.host, self.port))
        self.inputs.append(self.sock)
        self.outputs.append(self.sock)

    # 根据待发送消息的类型做不同处理
    def add_msg(self, _type, msg, data):
        # 添加json格式的待发送的数据至消息队列
        if _type == msgtype.FILE:
            filename = data['filename']
            basename = os.path.basename(filename)
            to = data['to']
            fileinfo_data = {'to': to, 'filename': basename, 'filesize': os.path.getsize(filename)}
            fileinfo = json.dumps({'type': _type, 'msg': 0, 'data': fileinfo_data})
            self.sock.send(fileinfo.encode('utf-8'))
            time.sleep(0.2)  # 防止沾包
            with open(filename, 'rb') as f:
                file_data = f.read(1024)
                while file_data:
                    self.sock.send(file_data)
                    file_data = f.read(1024)
            end_info = json.dumps({'type': _type, 'msg': 1, 'data': ''})
            self.sock.send(end_info.encode('utf-8'))  # 发送结束消息

        else:  # 文本消息
            send_msg = json.dumps({'type': _type, 'msg': msg, 'data': data})
            self.send_msg_queue.put(send_msg.encode('utf-8'))


if __name__ == '__main__':
    client = Client('127.0.0.1', 5000)
    client.connect()
    client_thread = ClientThread(client)
    client_thread.start()
