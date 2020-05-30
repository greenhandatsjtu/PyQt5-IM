# -*- coding: utf-8 -*-
"""
选择表情的窗口
"""
import sys

import qtawesome as qta
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import *

from resource import emoji


class EmojiWidget(QTableWidget):
    emoji_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.move(0, 0)
        self.setWindowTitle('表情')
        self.setStyleSheet('font-size: 30px')
        self.setWindowIcon(qta.icon('fa5.smile'))
        self.setRowCount(18)
        self.setColumnCount(6)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setVisible(False)
        for i in range(18):
            self.setRowHeight(i, 20)
            for j in range(6):
                item = QTableWidgetItem(emoji.emojis[i * 6 + j])
                item.setTextAlignment(Qt.AlignCenter)
                self.setItem(i, j, item)
                self.setColumnWidth(j, 20)
        self.itemClicked.connect(self.get)

    def get(self):
        try:
            self.emoji_signal.emit(self.selectedItems()[0].text())
        except Exception as e:
            print(e)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    emojia = EmojiWidget()
    emojia.show()
    sys.exit(app.exec_())
