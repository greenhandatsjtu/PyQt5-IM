import json
import queue
import select
import socket
import time

import pymysql

from resource import msgtype


# 构造json格式的待发送的消息
def construct_msg(_type, msg, data):
    return json.dumps({'type': _type, 'msg': msg, 'data': data})


class Server:
    def __init__(self, host, port):
        self.conn = None
        self.data = ""  # 接受的数据
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.HOST = host
        self.PORT = port
        self.sock.bind((self.HOST, self.PORT))  # 套接字绑定到指定地址
        self.inputs = []  # 传入列表
        self.outputs = []  # 传出列表
        self.inputs.append(self.sock)  # 将sock加入传入列表，可以监控连接请求
        self.msg_queues = {}  # 这个字典用来存放不同连接的消息队列
        self.online_users = []  # 存放在线用户信息
        self.online_users.append([])  # 第0行存放用户名
        self.online_users.append([])  # 第1行存放host和port
        self.groups = {'大厅': self.online_users[0]}

        # 连接数据库
        try:
            self.db = pymysql.connect(host='localhost', user='', passwd='', db='IM')
        except Exception as e:
            print(e)
            print("请确保数据库在运行中！")
            exit(-1)
        self.cur = self.db.cursor()

        # 从数据库取得群组的相关信息
        self.cur.execute('select id,name from `group`')
        result = self.cur.fetchall()
        for i in result:
            self.groups[i[1]] = []
            self.cur.execute("""select name from user
                                where id in 
                                (select  user_id from group_user
                                where group_id=%s)""" % i[0])
            user_result = self.cur.fetchall()
            for j in user_result:
                self.groups[i[1]].append(j[0])

    # 广播
    def broadcast(self, msg, users):
        for i in users:
            if i in self.online_users[0]:
                to_sock = self.outputs[self.online_users[0].index(i)]
                self.msg_queues[to_sock].put(msg)

    # 向每位用户发送同步消息
    def sendSync(self):
        for i in self.online_users[0]:
            in_groups = []  # 该用户在的群组
            for group, users in self.groups.items():
                if i in users:
                    in_groups.append(group)
            groups_and_users = {'groups': in_groups, 'users': self.online_users[0]}
            msg = construct_msg(msgtype.SYNC, '', groups_and_users)
            to_sock = self.outputs[self.online_users[0].index(i)]
            self.msg_queues[to_sock].put(msg.encode('utf-8'))

    def handle_msg(self, msg, sock):
        msg_dict = json.loads(msg)
        if msg_dict['type'] == msgtype.LOGIN:  # 登录消息
            usr_name = msg_dict['data']['name']
            passwd = msg_dict['data']['passwd']
            if not self.cur.execute("select * from user where name = '%s'" % usr_name):
                # 新用户
                self.cur.execute("insert into user (name, password) values('%s', '%s')" % (usr_name, passwd))
                self.db.commit()
            elif not self.cur.execute(
                    """
                    select * from user
                    where name = '%s' and password = '%s'
                    """ % (usr_name, passwd)) or usr_name in self.online_users[0]:
                # 如果用户密码错误或用户已登录
                msg = construct_msg(msgtype.ERR, 'wrong username or password', '')
                self.msg_queues[sock].put(msg.encode('utf-8'))  # 向该连接的消息队列放入回应
                return

            self.online_users[0].append(usr_name)  # 添加到在线用户列表第0行
            self.online_users[1].append(sock.getpeername())  # host和port添加到在线用户列表第1行
            self.sendSync()

        elif msg_dict['type'] == msgtype.TEXT:  # 聊天消息
            data = msg_dict['data']
            if data['to'] in self.online_users[0]:
                send_data = {'from': self.online_users[0][self.online_users[1].index(sock.getpeername())],
                             'text': data['text']}
                msg = construct_msg(msgtype.TEXT, '', send_data)
                to_sock = self.outputs[self.online_users[0].index(data['to'])]  # 根据用户名查找socket
                self.msg_queues[to_sock].put(msg.encode('utf-8'))  # 向目标连接的消息队列放入回应
            elif data['to'] in self.groups:
                send_data = {'from': data['to'],  # 群族名
                             'user': self.online_users[0][self.online_users[1].index(sock.getpeername())],  # 用户名
                             'text': data['text']}
                msg = construct_msg(msgtype.TEXT, 'group', send_data)
                self.broadcast(msg.encode('utf-8'), self.groups[data['to']])
        elif msg_dict['type'] == msgtype.FILE:
            msg = msg_dict['msg']
            if msg != 0:
                return
            data_dict = msg_dict['data']
            filename = data_dict['filename']
            expected_size = data_dict['filesize']
            to = data_dict['to']
            from_user = self.online_users[0][self.online_users[1].index(sock.getpeername())]
            if to in self.online_users[0]:
                if to == from_user:
                    return
                send_data = {'from': from_user,
                             'filename': filename, 'filesize': expected_size}
                to_sock = self.outputs[self.online_users[0].index(to)]  # 根据用户名查找socket
                msg = construct_msg(msgtype.FILE, 0, send_data)
                to_sock.send(msg.encode('utf-8'))
                time.sleep(0.2)  # 防止沾包
                size = 0
                while size < expected_size:
                    if expected_size - size < 1024:
                        data = sock.recv(expected_size - size)
                    else:
                        data = sock.recv(1024)
                    to_sock.send(data)
                    size += len(data)
                self.data = sock.recv(1024)
                msg = json.loads(self.data)['msg']
                if msg != 1:
                    return
                end_msg = construct_msg(msgtype.FILE, 1, '')  # 发送完成
                to_sock.send(end_msg.encode('utf-8'))
            elif to in self.groups:
                send_data = {'from': to,
                             'user': from_user,
                             'filename': filename, 'filesize': expected_size}
                to_users = self.groups[to]
                to_socks = []
                for to_user in to_users:
                    if to_user == from_user or to_user not in self.online_users[0]:
                        continue
                    to_socks.append(self.outputs[self.online_users[0].index(to_user)])
                msg = construct_msg(msgtype.FILE, 0, send_data)
                for to_sock in to_socks:
                    to_sock.send(msg.encode('utf-8'))
                time.sleep(0.2)  # 防止沾包
                size = 0
                while size < expected_size:
                    if expected_size - size < 1024:
                        data = sock.recv(expected_size - size)
                    else:
                        data = sock.recv(1024)
                    for to_sock in to_socks:
                        to_sock.send(data)
                    size += len(data)
                self.data = sock.recv(1024)
                msg = json.loads(self.data)['msg']
                if msg != 1:
                    return
                end_msg = construct_msg(msgtype.FILE, 1, '')  # 发送完成
                for to_sock in to_socks:
                    to_sock.send(end_msg.encode('utf-8'))

    def send(self, msg):
        self.conn.send(msg)

    # 启动服务
    def up(self):
        self.sock.listen(10)  # 可以挂起的最大连接数
        print('Server start at: %s:%s' % (self.HOST, self.PORT))
        print('wait for connection...')

        while True:
            readable, writable, exceptional = select.select(self.inputs, self.outputs, self.inputs)
            for r in readable:
                if r is self.sock:
                    # 表明有传入请求
                    conn, addr = self.sock.accept()
                    print('Connected by ', addr)
                    # conn.setblocking(False)
                    self.inputs.append(conn)
                    self.outputs.append(conn)
                    self.msg_queues[conn] = queue.Queue()  # 新建conn和消息队列的键值对

                else:
                    # 表示是已有的连接有传入数据
                    try:
                        self.data = r.recv(1024)
                    except:
                        pass

                    if self.data:
                        # 如果接收到数据
                        print(r.getpeername(), "says: ", self.data.decode('utf-8'))
                        self.handle_msg(self.data, r)
                        self.data = ''  # 清空data

                    else:
                        # 连接已断开
                        print("connection closed from ", r.getpeername())
                        if r in self.outputs:
                            # 就不再给它发消息了，移除outputs
                            self.outputs.remove(r)
                        self.inputs.remove(r)  # 从连接列表中也移去

                        # 从在线用户中移除
                        try:
                            index = self.online_users[1].index(r.getpeername())  # 对应的下标
                            del self.online_users[0][index]
                            del self.online_users[1][index]
                        except:
                            pass

                        self.sendSync()  # 向每位用户发去同步在线用户的消息
                        r.close()  # 关闭该连接

            for w in writable:
                if not self.msg_queues[w].empty():
                    data = self.msg_queues[w].get(False)
                    w.send(data)


if __name__ == "__main__":
    server = Server('localhost', 5000)
    server.up()
