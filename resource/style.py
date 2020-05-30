"""
用于美化界面的qss
"""

Aqua = """
#login{
	font-weight: bold;
	font-size: 25px;
}

QListWidget#message{
font-size: 40px;
font-family: Helvetica, YouYuan;
}

QListWidget#message::item{
min-height: 100px;
}
/*去掉item虚线边框*/
QListWidget, QListView, QTreeWidget, QTreeView {
    outline: 0px;
}
/*设置左侧选项的最小最大宽度,文字颜色和背景颜色*/
QListWidget#userlist {
    min-width: 180px;
    max-width: 180px;
    color: white;
    background: #0089A7;
}

/*鼠标悬停颜色*/
HistoryPanel::item:hover {
    background: rgb(52, 52, 52);
}

QWidget{
font-family:Arial,Helvetica,sans-serif;font-size:100%;
}

QListWidget#message{
    background: #CAE1FF;
}

QTextEdit#textEdit{
    background: #BDC0BA;
    font-size: 45px;
    font-family:Microsoft Yahei;
    border-width: 0px;
    height: 100px;
}

#textEdit:hover{
    background: #CFCFCF;
}

#textEdit:focus{
    background: white;
}

#name{
min-height: 100px;
font-size: 40px;
background: #EEEEE0;
color: #005CAF;
text-align: center;
font-family: FZYaoti;
font-weight: bold;
}

/*被选中时的背景颜色和左边框颜色*/
QListWidget#userlist::item:selected {
    background: rgb(52, 52, 52);
    border-left: 4px solid rgb(9, 187, 7);
    color: white;
}

#userlist::item:hover{
    background: #4169E1;
}

QMainWindow {
	background-color:#ececec;
}

QTextEdit {
	border-width: 1px;
	border-style: solid;
	border-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgba(0, 113, 255, 255), stop:1 rgba(91, 171, 252, 255));
}
QPlainTextEdit {
	border-width: 1px;
	border-style: solid;
	border-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgba(0, 113, 255, 255), stop:1 rgba(91, 171, 252, 255));
}
QToolButton {
	border-style: solid;
	border-top-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgb(215, 215, 215), stop:1 rgb(222, 222, 222));
	border-right-color: qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgb(217, 217, 217), stop:1 rgb(227, 227, 227));
	border-left-color: qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgb(227, 227, 227), stop:1 rgb(217, 217, 217));
	border-bottom-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgb(215, 215, 215), stop:1 rgb(222, 222, 222));
	border-width: 1px;
	border-radius: 5px;
	color: rgb(0,0,0);
	padding: 2px;
	background-color: rgb(255,255,255);
}
QToolButton:hover{
	border-style: solid;
	border-top-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgb(195, 195, 195), stop:1 rgb(222, 222, 222));
	border-right-color: qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgb(197, 197, 197), stop:1 rgb(227, 227, 227));
	border-left-color: qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgb(227, 227, 227), stop:1 rgb(197, 197, 197));
	border-bottom-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgb(195, 195, 195), stop:1 rgb(222, 222, 222));
	border-width: 1px;
	border-radius: 5px;
	color: rgb(0,0,0);
	padding: 2px;
	background-color: rgb(255,255,255);
}
QToolButton:pressed{
	border-style: solid;
	border-top-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgb(215, 215, 215), stop:1 rgb(222, 222, 222));
	border-right-color: qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgb(217, 217, 217), stop:1 rgb(227, 227, 227));
	border-left-color: qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgb(227, 227, 227), stop:1 rgb(217, 217, 217));
	border-bottom-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgb(215, 215, 215), stop:1 rgb(222, 222, 222));
	border-width: 1px;
	border-radius: 5px;
	color: rgb(0,0,0);
	padding: 2px;
	background-color: rgb(142,142,142);
}
QPushButton{
	border-style: solid;
	border-top-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgb(215, 215, 215), stop:1 rgb(222, 222, 222));
	border-right-color: qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgb(217, 217, 217), stop:1 rgb(227, 227, 227));
	border-left-color: qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgb(227, 227, 227), stop:1 rgb(217, 217, 217));
	border-bottom-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgb(215, 215, 215), stop:1 rgb(222, 222, 222));
	border-width: 1px;
	border-radius: 5px;
	color: rgb(0,0,0);
	padding: 2px;
	background-color: rgb(255,255,255);
}
QPushButton::default{
	border-style: solid;
	border-top-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgb(215, 215, 215), stop:1 rgb(222, 222, 222));
	border-right-color: qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgb(217, 217, 217), stop:1 rgb(227, 227, 227));
	border-left-color: qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgb(227, 227, 227), stop:1 rgb(217, 217, 217));
	border-bottom-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgb(215, 215, 215), stop:1 rgb(222, 222, 222));
	border-width: 1px;
	border-radius: 5px;
	color: rgb(0,0,0);
	padding: 2px;
	background-color: rgb(255,255,255);
}
QPushButton:hover{
	border-style: solid;
	border-top-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgb(195, 195, 195), stop:1 rgb(222, 222, 222));
	border-right-color: qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgb(197, 197, 197), stop:1 rgb(227, 227, 227));
	border-left-color: qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgb(227, 227, 227), stop:1 rgb(197, 197, 197));
	border-bottom-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgb(195, 195, 195), stop:1 rgb(222, 222, 222));
	border-width: 4px;
	border-radius: 5px;
	color: rgb(0,0,0);
	padding: 2px;
	background-color: #87CEFA;
}
QPushButton:pressed{
	border-style: solid;
	border-top-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgb(215, 215, 215), stop:1 rgb(222, 222, 222));
	border-right-color: qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgb(217, 217, 217), stop:1 rgb(227, 227, 227));
	border-left-color: qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgb(227, 227, 227), stop:1 rgb(217, 217, 217));
	border-bottom-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgb(215, 215, 215), stop:1 rgb(222, 222, 222));
	border-width: 1px;
	border-radius: 5px;
	color: rgb(0,0,0);
	padding: 2px;
	background-color: rgb(142,142,142);
}
QPushButton:disabled{
	border-style: solid;
	border-top-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgb(215, 215, 215), stop:1 rgb(222, 222, 222));
	border-right-color: qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgb(217, 217, 217), stop:1 rgb(227, 227, 227));
	border-left-color: qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgb(227, 227, 227), stop:1 rgb(217, 217, 217));
	border-bottom-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgb(215, 215, 215), stop:1 rgb(222, 222, 222));
	border-width: 1px;
	border-radius: 5px;
	color: #808086;
	padding: 2px;
	background-color: rgb(142,142,142);
}
QLineEdit {
	border-width: 1px; border-radius: 4px;
	border-style: solid;
	border-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgba(0, 113, 255, 255), stop:1 rgba(91, 171, 252, 255));
}


QScrollArea {
	color: #FFFFFF;
	background-color:#000000;
}

QScrollBar:horizontal {
	max-height: 20px;
	border: 1px transparent grey;
	margin: 0px 20px 0px 20px;
}
QScrollBar:vertical {
	max-width: 20px;
	border: 1px transparent grey;
	margin: 20px 0px 20px 0px;
}
QScrollBar::handle:horizontal {
	background: rgb(253,253,253);
	border-style: solid;
	border-width: 1px;
	border-color: rgb(207,207,207);
	border-radius: 7px;
	min-width: 25px;
}
QScrollBar::handle:horizontal:hover {
	background: rgb(253,253,253);
	border-style: solid;
	border-width: 1px;
	border-color: rgb(147, 200, 200);
	border-radius: 7px;
	min-width: 25px;
}
QScrollBar::handle:vertical {
	background: rgb(253,253,253);
	border-style: solid;
	border-width: 1px;
	border-color: rgb(207,207,207);
	border-radius: 7px;
	min-height: 25px;
}
QScrollBar::handle:vertical:hover {
	background: rgb(253,253,253);
	border-style: solid;
	border-width: 1px;
	border-color: rgb(147, 200, 200);
	border-radius: 7px;
	min-height: 25px;
}
QScrollBar::add-line:horizontal {
   border: 2px transparent grey;
   border-top-right-radius: 7px;
   border-bottom-right-radius: 7px;
   background: rgba(34, 142, 255, 255);
   width: 20px;
   subcontrol-position: right;
   subcontrol-origin: margin;
}
QScrollBar::add-line:horizontal:pressed {
   border: 2px transparent grey;
   border-top-right-radius: 7px;
   border-bottom-right-radius: 7px;
   background: rgb(181,181,181);
   width: 20px;
   subcontrol-position: right;
   subcontrol-origin: margin;
}
QScrollBar::add-line:vertical {
   border: 2px transparent grey;
   border-bottom-left-radius: 7px;
   border-bottom-right-radius: 7px;
   background: rgba(34, 142, 255, 255);
   height: 20px;
   subcontrol-position: bottom;
   subcontrol-origin: margin;
}
QScrollBar::add-line:vertical:pressed {
   border: 2px transparent grey;
   border-bottom-left-radius: 7px;
   border-bottom-right-radius: 7px;
   background: rgb(181,181,181);
   height: 20px;
   subcontrol-position: bottom;
   subcontrol-origin: margin;
}
QScrollBar::sub-line:horizontal {
   border: 2px transparent grey;
   border-top-left-radius: 7px;
   border-bottom-left-radius: 7px;
   background: rgba(34, 142, 255, 255);
   width: 20px;
   subcontrol-position: left;
   subcontrol-origin: margin;
}
QScrollBar::sub-line:horizontal:pressed {
   border: 2px transparent grey;
   border-top-left-radius: 7px;
   border-bottom-left-radius: 7px;
   background: rgb(181,181,181);
   width: 20px;
   subcontrol-position: left;
   subcontrol-origin: margin;
}
QScrollBar::sub-line:vertical {
   border: 2px transparent grey;
   border-top-left-radius: 7px;
   border-top-right-radius: 7px;
   background: rgba(34, 142, 255, 255);
   height: 20px;
   subcontrol-position: top;
   subcontrol-origin: margin;
}
QScrollBar::sub-line:vertical:pressed {
   border: 2px transparent grey;
   border-top-left-radius: 7px;
   border-top-right-radius: 7px;
   background: rgb(181,181,181);
   height: 20px;
   subcontrol-position: top;
   subcontrol-origin: margin;
}
QScrollBar::left-arrow:horizontal {
   border: 1px transparent grey;
   border-top-left-radius: 3px;
   border-bottom-left-radius: 3px;
   width: 6px;
   height: 6px;
   background: white;
}
QScrollBar::right-arrow:horizontal {
   border: 1px transparent grey;
   border-top-right-radius: 3px;
   border-bottom-right-radius: 3px;
   width: 6px;
   height: 6px;
   background: white;
}
QScrollBar::up-arrow:vertical {
   border: 1px transparent grey;
   border-top-left-radius: 3px;
   border-top-right-radius: 3px;
   width: 6px;
   height: 6px;
   background: white;
}
QScrollBar::down-arrow:vertical {
   border: 1px transparent grey;
   border-bottom-left-radius: 3px;
   border-bottom-right-radius: 3px;
   width: 6px;
   height: 6px;
   background: white;
}
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
   background: none;
}
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
   background: none;
}
"""
