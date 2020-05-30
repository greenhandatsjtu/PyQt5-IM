# -*- coding: utf-8 -*-
"""
客户端界面
"""
import qtawesome as qta
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

from resource import style
from widgets.chatWidget import ChatWidget
from widgets.emojiWidget import EmojiWidget


class MainWidget(QWidget):

    def __init__(self):
        super(MainWidget, self).__init__()
        self.resize(1200, 800)
        self.setWindowTitle('Sun-IM')
        self.setWindowIcon(qta.icon('fa5.comment-dots'))

        # 设置任系统托盘
        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(qta.icon('fa5.comment-dots', color='white'))
        self.tray.setVisible(True)

        # 表情的表格
        self.emojis = EmojiWidget()
        self.emojis.resize(580, 340)

        # 左右布局(左边一个QListWidget + 右边QStackedWidget)
        layout = QHBoxLayout(self, spacing=0)
        layout1 = QVBoxLayout(self, spacing=0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout1.setContentsMargins(0, 0, 0, 0)
        # 左侧列表
        self.nameLabel = QLabel('游客' + '\ud83d\ude00')
        self.nameLabel.setObjectName('name')
        self.nameLabel.setAlignment(Qt.AlignCenter)
        self.loginButton = QPushButton(self)
        self.loginButton.setText('登录/注册')
        self.loginButton.setObjectName('login')
        self.loginButton.setIcon(qta.icon('fa5.user'))
        self.loginButton.setFixedHeight(80)
        self.userListWidget = QListWidget(self)
        self.userListWidget.setObjectName('userlist')

        layout1.addWidget(self.nameLabel)
        layout1.addWidget(self.loginButton)
        layout1.addWidget(self.userListWidget)
        layout.addLayout(layout1)

        # 右侧层叠窗口
        self.stackedWidget = QStackedWidget(self)
        layout.addWidget(self.stackedWidget)
        self.initUi()

    # 初始化界面
    def initUi(self):
        # 去掉边框
        self.userListWidget.setFrameShape(QListWidget.NoFrame)
        # 隐藏滚动条
        self.userListWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.userListWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        chatWidget = ChatWidget()
        chatWidget.setObjectName('unlogin')  # 未登录
        self.stackedWidget.addWidget(chatWidget)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    app.setStyleSheet(style.Aqua)
    w = MainWidget()
    w.show()
    sys.exit(app.exec_())
