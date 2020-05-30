# -*- coding: utf-8 -*-
"""
聊天窗口，包含聊天框、输入框和几个按钮
"""
import qtawesome as qta
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from resource import style


class ChatWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(1200, 800)
        layout = QVBoxLayout(self)  # 上下布局
        layout1 = QHBoxLayout(self)  # 左右布局
        layout2 = QVBoxLayout(self)  # 上下布局
        layout3 = QHBoxLayout(self)
        layout1.setContentsMargins(0, 0, 0, 0)
        layout2.setContentsMargins(0, 0, 0, 0)

        # 输入框
        self.msgList = QListWidget(self)
        self.msgList.setObjectName('message')
        layout.addWidget(self.msgList)
        self.msgEdit = QTextEdit(self)
        self.msgEdit.setObjectName('textEdit')
        self.msgList.setFrameShape(QListWidget.NoFrame)
        self.msgEdit.setFrameShape(QListWidget.NoFrame)
        self.msgEdit.setFixedHeight(300)
        # 隐藏滚动条
        self.msgList.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        layout1.addWidget(self.msgEdit)

        # 几个按钮
        self.emojiButton = QPushButton()
        self.emojiButton.setText('表情')
        self.emojiButton.setEnabled(False)
        self.emojiButton.setFixedSize(100, 80)
        self.fileButton = QPushButton()
        self.fileButton.setText('文件')
        self.fileButton.setEnabled(False)
        self.fileButton.setFixedSize(100, 80)
        self.voiceButton = QPushButton()
        self.voiceButton.setText('语音')
        self.voiceButton.setToolTip('按下开始录音，松开结束录音并发送')
        self.voiceButton.setEnabled(False)
        self.voiceButton.setFixedSize(100, 80)
        self.sendButton = QPushButton()
        self.sendButton.setFixedSize(160, 80)
        self.sendButton.setText('发送')
        self.sendButton.setEnabled(False)
        self.emojiButton.setIcon(qta.icon('fa5.laugh'))
        self.sendButton.setIcon(qta.icon('fa.send'))
        self.fileButton.setIcon(qta.icon('fa.file'))
        self.voiceButton.setIcon(qta.icon('fa.microphone'))

        layout3.addWidget(self.emojiButton, 0, Qt.AlignLeft)
        layout3.addWidget(self.fileButton, 0, Qt.AlignRight)
        layout2.addLayout(layout3)
        layout2.addWidget(self.voiceButton, 0, Qt.AlignCenter)
        layout2.addWidget(self.sendButton, 0, Qt.AlignCenter)
        layout1.addLayout(layout2)
        layout.addLayout(layout1)


styleSheet = """
QPushButton{
min-width: 120px;
max-width: 240px
}
"""

if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    app.setStyleSheet(style.Aqua)
    w = ChatWidget()
    w.show()
    sys.exit(app.exec_())
