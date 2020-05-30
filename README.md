# PyQt5-IM
PyQt5 based IM    基于PyQt5的聊天程序

## 主要功能

+ 多用户间一对一聊天
+ 群组聊天
+ 文件传输
+ 使用表情
+ 语音消息
+ 实时更新在线用户列表
+ 注册用户
+ 系统通知新消息

## 使用方法

2. 进入工程目录`IM`，执行如下命令安装依赖库：

   ```bash
   pip3 install -r requirements.txt
   ```

   > 注：若是Linux系统，可能需要使用如下命令安装PyQt：
   >
   > ```bash
   > sudo apt-get install python3-pyqt5
   > ```

3. MySQL数据库中新建schema：

   ```mysql
   create schema im;
   ```

4. 命令行中执行如下命令导入数据库：

   ```bash
   mysql -uroot -p im < dump.sql
   ```

5. 修改`server.py`文件中如下一行，将MySQL用户名和密码改成自己的

   ```python
   self.db = pymysql.connect(host='localhost', user='user', passwd='passwd', db='IM')
   ```

6. 启动服务器

   ```bash
   python server.py
   ```

7. 启动客户端，用户有"admin"、"kirito"、"asuna"、"alice"、"saber"，密码均为“test”，自行选择一个登录，或者也可注册

   ```bash
   python app.py
   ```

## 项目目录

```
   |-- IM
       |-- app.py	客户端程序入口
       |-- client.py	客户端socket
       |-- clientthread.py	客户端socket线程
       |-- dump.sql		数据库备份
       |-- requirements.txt	库依赖
       |-- server.py	服务器端程序
       |-- ui.py	客户端界面
       |-- resource
       |   |-- emoji.py		存储所有表情（ascii）
       |   |-- msgtype.py	存储所有消息类型
       |   |-- style.py		GUI样式
       |   |-- __init__.py
       |-- widgets
       |   |-- chatWidget.py	聊天窗口
       |   |-- dialog.py		登录对话框
       |   |-- dialog.ui		qt的ui文件，生成dialog.py
       |   |-- emojiWidget.py	表情选择框
       |   |-- fileWidget.py	文件
       |   |-- __init__.py
```

## 主要算法

1. 整个聊天程序用到最多是`PyQt5`的 **signal&slot**（信号与槽）机制。这是`Qt`中的核心机制，用以实现**对象之间的通信**，当然`PyQt`中也移植了这个机制。`PyQt5`中信号和槽通过connect()方法来连接。当指定事件发生时，信号会被发射（emit），信号连接的槽就会被调用。这个机制比较重要的特性是**信号和槽的连接可能会跨线程**。所以通过这个机制，我就能完美解决**后端线程与主线程（GUI）之间的通信**问题：只需将诸如消息等封装成信号，并连接到主线程的相关逻辑即可。

   例如，在`ClientThread`类中，我定义了三个signal：

   ```python
   # clientthread.py
   
   text_signal = pyqtSignal(dict)  # 定义字典型的signal，用于发送文本消息
   usr_signal = pyqtSignal(dict)  # 定义字典型的signal，用于发送同步用户消息
   file_signal = pyqtSignal(dict)  # 字典型signal，用于发送文件信号
   ```

   在主线程中，我们将这几个信号连接到相关的函数即可

   ```python
   # app.py
   
   self.client_thread.text_signal.connect(self.showText)  # 显示文本消息
   self.client_thread.usr_signal.connect(self.showUserList)  # 更新在线用户
   self.client_thread.file_signal.connect(self.showFile)  # 显示文件消息
   ```

   之前提到，信号要被发射，其连接的函数才会被调用，所以接下来我们回到`clientthread.py`文件中，emit这些信号，比如发射文本消息的信号

   ```python
   self.text_signal.emit(msg_dict['data'])
   ```

   这样，当后台线程接受到文本消息后，发送`text_signal`，`App.showText`便会被调用，显示文本消息，成功用比较简单地方式实现了前后端分离以及线程间通信的问题。

   在`PyQt`中，每一个`QObject`对象和所有继承自`QWidget`的控件都支持信号和槽，例如在`app.py`中我将“点击登录按钮”连接到“显示登录框”

   ```python
   self.loginButton.clicked.connect(self.showLoginDialog)
   ```

2. 客户端和服务器都用到了`select.select()`方法来实现非阻塞式I/O传送和接收消息。`select`是python的自带库，详细说明可以看[官方文档](https://docs.python.org/3.7/library/select.html)。select()方法**直接调用操作系统的IO接口**，它非阻塞地监控sockets等所有带`fileno()`方法的文件句柄何时变成readable（可读，即有传入消息） 和writeable（可写，即可发送消息）, 或者通信错误。具体使用时，需要向`select()`方法传进三个list，第一个是等待直至可读的socket列表，第二个等待直至可写的socket列表，第三个列表是等待直至出错的socket列表；`select()`非阻塞地监控它们，若有一个list出现满足条件的socket，就返回它的socket子集，若均不满足条件，则线程继续执行。在我的程序中，我在一个`while`循环中调用`select()`，传入三个参数：待输出的socket列表，待输入的socket列表和待输入的socket列表，并且当`select()`返回可读或可写的列表时，才进行socket的收发操作，这很好地解决了`socket.recv()`和`socket.send()`的阻塞问题。

   例如，在`server.py`中：

   ```python
   while True:
       readable, writable, exceptional = select.select(self.inputs, self.outputs, self.inputs)
       for r in readable:
           if r is self.sock:
               # 表明有传入请求
               #进行添加在线用户等操作
   
           else:
               # 表示是已有的连接有传入数据
               try:
                   self.data = r.recv(1024)  # 尝试接收数据
               except:
                   pass
   
               if self.data:
                   # 接收到数据
   
               else:
                   # 连接已断开
                   # 进行移除该用户，并关闭socket连接等操作
   
       for w in writable:
           # 从队列中取出消息并发送
   ```

   以上是服务器端收发数据的主要框架，具体代码可以看`server.py`。

3. 客户端和服务器都用到了python的自带库`Queue`，即队列。拿服务器端来说，因为当服务器接收到某个用户发来的消息时，需要转发给另外一个用户，但是若服务器此时正在转发另一则消息到该用户，就会发生消息的混乱。所以需要用到队列，当消息传来时，不是立即转发出去，而是存到对方用户的消息队列中：

   ```python
   # server.py
   
   to_sock = self.outputs[self.online_users[0].index(data['to'])]  # 根据用户名查找socket
   self.msg_queues[to_sock].put(msg.encode('utf-8'))  # 向目标连接的消息队列放入回应
   ```

   `msg_queues`是服务器维护的一个所有socket的消息队列。

   当该socket可以写时，说明消息可以发送了，若其消息队列非空，服务器则从该队列中取消息，并且发送。

   ```python
   # server.py
   
   for w in writable:
       if not self.msg_queues[w].empty():
       	data = self.msg_queues[w].get(False)
       	w.send(data)
   ```
