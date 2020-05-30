# -*- coding: utf-8 -*-
"""
客户端入口程序
"""
import hashlib
import os
import sys
import time

import qtawesome as qta
from PyQt5 import QtCore, QtMultimedia
from PyQt5.QtCore import Qt, QSize, QUrl, QEventLoop
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtMultimedia import QAudioRecorder, QAudioEncoderSettings
from PyQt5.QtWidgets import *

from client import Client
from clientthread import ClientThread
from resource import style, msgtype
from ui import MainWidget
from widgets.chatWidget import ChatWidget
from widgets.dialog import LoginDialog
from widgets.fileWidget import FileWidget


class App(MainWidget):
    client = Client('localhost', 5000)
    client_thread = ClientThread(client)  # 后台线程

    def __init__(self):
        super(App, self).__init__()
        self.loginButton.clicked.connect(self.showLoginDialog)
        self.client_thread.text_signal.connect(self.showText)  # 显示文本消息
        self.client_thread.usr_signal.connect(self.showUserList)  # 更新在线用户
        self.client_thread.file_signal.connect(self.showFile)  # 显示文件消息
        self.emojis.emoji_signal.connect(self.addEmoji)

        # 通过QListWidget的当前item变化来切换QStackedWidget中的序号
        self.userListWidget.currentRowChanged.connect(
            self.dialogChanged)

        self.usrList = []  # 保存上一次的在线用户列表
        self.groupList = []  # 群组列表

        self.md5 = hashlib.md5()  # 用于加密密码

        # 录音机
        self.recorder = QAudioRecorder(self)
        settings = QAudioEncoderSettings()
        settings.setChannelCount(2)
        settings.setSampleRate(16000)
        self.recorder.setEncodingSettings(settings)

    # 处理对话用户改变
    def dialogChanged(self, i):
        # 通过QListWidget的当前item变化来切换QStackedWidget中的序号
        self.stackedWidget.setCurrentIndex(i)

        # enable当前chatWidget的所有按钮
        self.stackedWidget.currentWidget().emojiButton.setEnabled(True)
        self.stackedWidget.currentWidget().sendButton.setEnabled(True)
        self.stackedWidget.currentWidget().fileButton.setEnabled(True)
        self.stackedWidget.currentWidget().voiceButton.setEnabled(True)
        try:
            # 设置图标
            self.userListWidget.currentItem().setIcon(qta.icon('fa.check-circle', color='lightgreen'))
        except:
            pass

    # 显示登陆对话框
    def showLoginDialog(self):
        # 登录对话框
        self.d = LoginDialog()
        self.dialog = QDialog()
        self.d.setupUi(self.dialog)
        self.dialog.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.dialog.show()
        # 点击确认就调用login()进行登录操作
        self.d.buttonBox.accepted.connect(self.login)

    # 登录的相关操作
    def login(self):
        passwd = self.d.lineEdit_2.text()
        if len(passwd) == 0:
            print('密码不能为空！')
            QMessageBox.critical(self, "错误", "密码不能为空！", QMessageBox.Ok)
            return
        try:
            self.client.connect()
        except:
            print('连接服务器失败！')
            QMessageBox.critical(self, "错误", "连接服务器失败！", QMessageBox.Ok)
            return
        self.client_thread.start()  # 启动线程
        self.name = self.d.lineEdit.text()  # 用户名
        self.client.name = self.name

        # md5加密密码
        self.md5.update(passwd.encode('utf-8'))
        hashed_passwd = self.md5.hexdigest()

        data = {'name': self.name, 'passwd': hashed_passwd}
        self.nameLabel.setText('<u>' + self.name)
        self.client.add_msg(msgtype.LOGIN, '', data)  # 登录信息发给服务器验证
        self.stackedWidget.removeWidget(self.stackedWidget.findChild(ChatWidget, name='unlogin'))  # 移除未登录显示的界面
        # 关闭登录按钮
        self.loginButton.close()

        # 为用户建立文件夹
        if not os.path.exists('./temp/%s' % self.client.name):
            os.makedirs('./temp/%s' % self.client.name)

    # 发送文字消息
    def sendText(self):
        text = self.stackedWidget.currentWidget().msgEdit.toPlainText()
        if not len(text):
            return  # 长度为零，不发送
        try:
            to = self.userListWidget.selectedItems()[0].text()
        except:  # 出现异常是因为没有选择对话用户
            return
        if to != self.name:
            data = {'to': to, 'text': text}
            self.client.add_msg(msgtype.TEXT, '', data)
        self.stackedWidget.currentWidget().msgEdit.clear()  # 清空输入框

        # 显示在聊天记录中
        item = QListWidgetItem()
        item.setText(text)
        item.setBackground(QColor('#F19483'))
        item.setTextAlignment(Qt.AlignRight)
        self.stackedWidget.currentWidget().msgList.addItem(item)

    # 显示收到的文字消息
    def showText(self, msg):
        from_user = msg['from']
        text = msg['text']
        item = QListWidgetItem()
        if from_user in self.usrList:  # 一对一
            item.setText(text)
        elif from_user in self.groupList:  # 群聊
            user = msg['user']  # 发言用户
            if user == self.name:
                return
            item.setText('<%s>' % user + text)
        item.setTextAlignment(Qt.AlignLeft)
        item.setBackground(QColor('#F7D420'))
        chat = self.stackedWidget.findChild(ChatWidget, name=from_user)  # 找到对应的chatWidget插入新的消息
        chat.msgList.addItem(item)
        chat.msgList.setCurrentRow(chat.msgList.count() - 1)
        if from_user in self.usrList:
            if self.stackedWidget.currentIndex() != self.usrList.index(from_user) + len(self.groupList):
                # 如果当前没有和该用户对话，就显示未读图标，并弹出通知
                user = self.userListWidget.item(self.usrList.index(from_user) + len(self.groupList))
                user.setIcon(qta.icon('fa.circle', color='orange'))
                self.tray.showMessage(from_user, text, qta.icon('fa5.comment-alt', color='white'))
        elif from_user in self.groupList:
            if self.stackedWidget.currentIndex() != self.groupList.index(from_user):
                # 如果当前没有看这个群聊，就显示未读图标，并弹出通知
                user = self.userListWidget.item(self.groupList.index(from_user))
                user.setIcon(qta.icon('fa.circle', color='orange'))
                self.tray.showMessage(from_user, text, qta.icon('fa5.comment-alt', color='white'))

    # 更新在线用户列表和对应的chatWidget
    def showUserList(self, usr_list):
        users = usr_list['users']
        groups = usr_list['groups']

        # 群组
        for i in groups:
            if i not in self.groupList:
                # 添加右侧的chatWidget
                chatWidget = ChatWidget()
                chatWidget.setObjectName(i)
                chatWidget.emojiButton.clicked.connect(self.emojis.show)
                chatWidget.sendButton.clicked.connect(self.sendText)
                chatWidget.fileButton.clicked.connect(self.sendFile)
                chatWidget.voiceButton.pressed.connect(self.startRecord)
                chatWidget.voiceButton.released.connect(self.stopRecord)
                self.stackedWidget.addWidget(chatWidget)

                # 添加到左侧的用户列表
                item = QListWidgetItem(i)
                item.setSizeHint(QSize(16777215, 60))
                item.setTextAlignment(Qt.AlignCenter)
                item.setText(i)
                item.setIcon(qta.icon('fa.check-circle', color='lightgreen'))
                self.userListWidget.addItem(item)

        # 清空用户列表
        for i in range(len(groups), self.userListWidget.count()):
            self.userListWidget.takeItem(len(groups))

        # 用户
        for i in users:
            # 添加到用户列表
            item = QListWidgetItem(i)
            item.setSizeHint(QSize(16777215, 60))
            item.setTextAlignment(Qt.AlignCenter)
            item.setText(i)
            item.setIcon(qta.icon('fa.check-circle', color='lightgreen'))
            self.userListWidget.addItem(item)

        # 对于下线的用户，移除对应的chatWidget
        for i in self.stackedWidget.findChildren(ChatWidget):
            if i.objectName() not in users and i.objectName() not in groups:
                self.stackedWidget.removeWidget(i)

        for i in users:
            if i not in self.usrList:  # 新用户
                # 添加右侧的chatWidget
                chatWidget = ChatWidget()
                chatWidget.setObjectName(i)
                chatWidget.emojiButton.clicked.connect(self.emojis.show)
                chatWidget.sendButton.clicked.connect(self.sendText)
                chatWidget.fileButton.clicked.connect(self.sendFile)
                chatWidget.voiceButton.pressed.connect(self.startRecord)
                chatWidget.voiceButton.released.connect(self.stopRecord)
                self.stackedWidget.addWidget(chatWidget)

        self.usrList = users  # 更新用户列表
        self.groupList = groups  # 更新群组列表

    # 发送文件
    def sendFile(self):
        fileName, filetype = QFileDialog.getOpenFileName(self, "选取文件", "./")
        if len(fileName) == 0:
            return
        to = self.userListWidget.selectedItems()[0].text()  # 发送给的用户
        if to != self.name:
            self.client.add_msg(msgtype.FILE, '', {'to': to, 'filename': fileName})

        # 文件显示在聊天记录中
        item = QListWidgetItem()
        item.setSizeHint(QSize(200, 80))
        fileWidget = FileWidget(fileName, 0)
        item.setBackground(QColor('#F19483'))
        fileWidget.fileButton.setObjectName(fileName)
        fileWidget.fileButton.clicked.connect(self.openFile)
        self.stackedWidget.currentWidget().msgList.addItem(item)
        self.stackedWidget.currentWidget().msgList.setItemWidget(item, fileWidget)

    # 显示收到的文件
    def showFile(self, msg):
        from_user = msg['from']
        filename = msg['filename']
        chat = self.stackedWidget.findChild(ChatWidget, name=from_user)  # 找到对应的chatWidget插入新的消息
        if from_user in self.usrList:  # 一对一
            if self.stackedWidget.currentIndex() != self.usrList.index(from_user) + len(self.groupList):
                # 如果当前没有和该用户对话，就显示未读图标
                user = self.userListWidget.item(self.usrList.index(from_user) + len(self.groupList))
                user.setIcon(qta.icon('fa.circle', color='orange'))
                self.tray.showMessage(from_user, filename, qta.icon('fa5.file', color='white'))
        elif from_user in self.groupList:  # 群聊
            item = QListWidgetItem()
            item.setText('<%s>' % msg['user'])
            item.setBackground(QColor('#F7D420'))
            item.setSizeHint(QSize(200, 40))
            chat.msgList.addItem(item)
            if self.stackedWidget.currentIndex() != self.groupList.index(from_user):
                user = self.userListWidget.item(self.groupList.index(from_user))
                user.setIcon(qta.icon('fa.circle', color='orange'))
                self.tray.showMessage(from_user, filename, qta.icon('fa5.file', color='white'))

        # 文件显示在聊天记录中
        item = QListWidgetItem()
        item.setBackground(QColor('#F7D420'))
        item.setSizeHint(QSize(200, 80))
        fileWidget = FileWidget(filename, 1)
        fileWidget.fileButton.setObjectName('./temp/%s/' % self.name + filename)
        if filename.endswith('.wav'):  # 语音消息
            fileWidget.fileButton.clicked.connect(self.playVoice)
        else:
            fileWidget.fileButton.clicked.connect(self.openFile)
        chat.msgList.addItem(item)
        chat.msgList.setItemWidget(item, fileWidget)

    # 打开点击的文件
    def openFile(self):
        filename = self.sender().objectName()
        QDesktopServices.openUrl(QUrl.fromLocalFile(filename))

    # 开始录音
    def startRecord(self):
        print('开始录音...')
        self.stackedWidget.currentWidget().voiceButton.setIcon(qta.icon('fa.spinner'))  # 设置图标
        # 设置文件名
        self.voiceFileName = os.path.abspath('.') + '\\temp\\%s\\%s.wav' % (
            self.name, time.strftime('%Y%m%d%H%M%S', time.localtime()))
        print(self.voiceFileName)
        self.recorder.setOutputLocation(QUrl.fromLocalFile(self.voiceFileName))
        self.recorder.record()  # 开始录音

    # 停止录音并发送
    def stopRecord(self):
        self.stackedWidget.currentWidget().voiceButton.setIcon(qta.icon('fa.microphone'))
        self.recorder.stop()
        print('录音结束')
        to = self.userListWidget.selectedItems()[0].text()
        if to != self.name:
            self.client.add_msg(msgtype.FILE, '', {'to': to, 'filename': self.voiceFileName})
        item = QListWidgetItem()
        item.setSizeHint(QSize(200, 80))
        item.setBackground(QColor('#F19483'))
        fileWidget = FileWidget(self.voiceFileName, 0)
        fileWidget.fileButton.setObjectName(self.voiceFileName)
        fileWidget.fileButton.clicked.connect(self.playVoice)
        self.stackedWidget.currentWidget().msgList.addItem(item)
        self.stackedWidget.currentWidget().msgList.setItemWidget(item, fileWidget)

    # 播放语音
    def playVoice(self):
        print('playing ' + self.sender().objectName())
        sound = QtMultimedia.QSound(self.sender().objectName())  # 取得文件名
        sound.play()
        loop = QEventLoop()
        loop.exec()

    # 向输入框中添加选中的表情
    def addEmoji(self, emoji):
        self.stackedWidget.currentWidget().msgEdit.setText(
            self.stackedWidget.currentWidget().msgEdit.toPlainText() + emoji)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(style.Aqua)
    ui = App()
    ui.show()
    sys.exit(app.exec_())
