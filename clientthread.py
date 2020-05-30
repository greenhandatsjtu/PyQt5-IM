# -*- coding: utf-8 -*-
"""
后端线程
"""
import json
import select
import sys

from PyQt5.QtCore import *

from resource import msgtype


class ClientThread(QThread):
    text_signal = pyqtSignal(dict)  # 定义字典型的signal，用于发送文本消息
    usr_signal = pyqtSignal(dict)  # 定义字典型的signal，用于发送同步用户消息
    file_signal = pyqtSignal(dict)  # 字典型signal，用于发送文件信号

    def __init__(self, client):
        super().__init__()
        self.client = client

    # 处理服务器发过来的消息
    def handle_msg(self, msg):
        msg_dict = json.loads(msg)
        if msg_dict['type'] == msgtype.SYNC:  # 同步在线用户
            self.client.userList = msg_dict['data']
            self.usr_signal.emit(self.client.userList)
        elif msg_dict['type'] == msgtype.TEXT:  # 文字信息
            self.text_signal.emit(msg_dict['data'])
        elif msg_dict['type'] == msgtype.FILE:  # 文件消息
            if json.loads(msg)['msg'] != 0:
                return
            data_dict = msg_dict['data']
            send_usr = data_dict['from']
            filename = data_dict['filename']
            expected_size = data_dict['filesize']
            with open('./temp/%s/%s' % (self.client.name, filename), 'wb') as f:
                size = 0
                while size < expected_size:
                    if expected_size - size < 1024:
                        data = self.client.sock.recv(expected_size - size)
                    else:
                        data = self.client.sock.recv(1024)
                    f.write(data)
                    size += len(data)
            data = self.client.sock.recv(1024).decode('utf-8')
            print(data)
            msg = json.loads(data)['msg']
            if msg != 1:
                return
            try:
                # 群聊
                self.file_signal.emit({'from': send_usr, 'filename': filename, 'user': data_dict['user']})
            except:
                # 一对一
                self.file_signal.emit({'from': send_usr, 'filename': filename})
        elif msg_dict['type'] == msgtype.ERR:  # 错误消息
            sys.exit()

    # 覆盖Qthread的run方法，进行接收和发送信息的工作
    def run(self):
        while True:
            readable, writable, exceptional = select.select(self.client.inputs, self.client.outputs, self.client.inputs)
            for r in readable:
                try:
                    self.client.msg = r.recv(1024)
                except Exception as e:
                    print(e)
                try:
                    self.client.msg = self.client.msg.decode('utf-8')
                except Exception as e:
                    print(e)
                if self.client.msg:  # 如果收到消息
                    print(" receive: ", self.client.msg)
                    self.handle_msg(self.client.msg)
                    self.client.msg = ''
                else:  # 否则断开连接
                    print("connection closed.")
                    self.client.inputs.remove(r)
                    exit(-1)
            for w in writable:
                if not self.client.send_msg_queue.empty():
                    w.send(self.client.send_msg_queue.get_nowait())
