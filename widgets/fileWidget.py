# -*- coding: utf-8 -*-
"""
用来显示文件（包括语音）
"""
import os

import qtawesome as qta
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *


class FileWidget(QWidget):
    def __init__(self, fileName, left):
        super().__init__()
        layout1 = QHBoxLayout(self, spacing=0)  # 左右布局
        self.fileButton = QPushButton()
        if fileName.endswith('.wav'):
            self.fileButton.setIcon(qta.icon('fa.play'))
            self.fileButton.setText('(语音消息)')
            self.fileButton.setToolTip('点击播放语音消息')
        else:
            self.fileButton.setIcon(qta.icon('fa5.file'))
            self.fileButton.setText(os.path.basename(fileName))
            self.fileButton.setToolTip('点击打开文件')
        self.fileButton.setMinimumSize(60, 60)
        if left:
            layout1.addWidget(self.fileButton, 0, Qt.AlignLeft)
            layout1.setContentsMargins(40, 10, 0, 10)
        else:
            layout1.addWidget(self.fileButton, 0, Qt.AlignRight)
            layout1.setContentsMargins(0, 10, 40, 10)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    w = FileWidget('../temp/kirito/test.gif', 1)
    w.show()
    sys.exit(app.exec_())
