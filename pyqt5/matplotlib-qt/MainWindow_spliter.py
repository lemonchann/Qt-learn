# -*- coding: utf-8 -*-


import sys
import os

from PyQt5.QtCore import Qt, QPointF, pyqtSignal
from PyQt5.QtGui import QPainter, QPolygonF,QFont
from PyQt5.QtWidgets import QTextEdit, QMessageBox,QHBoxLayout,QVBoxLayout, QWidget,\
	 QFileDialog,QAction, QSplitter, QApplication, QMainWindow, QSplitterHandle

from MyMplCanvas import *

class MainWindow(QMainWindow):
	def __init__(self):
		QMainWindow.__init__(self)
		#创建mainWidget,取代原来的mainwidget,并布置主界面布局
		self.mainWidget = QWidget(self)
		self.setCentralWidget(self.mainWidget)
		self.hBox = QHBoxLayout(self.mainWidget)
		

		#创建multilayer实例，这里之后需要修改，应只创建一个实例
		#顶部
		self.widget1 = MyDynamicMplCanvas()
		self.widget2 = MyDynamicMplCanvas()
		self.widget3 = MyDynamicMplCanvas()
		self.widget4 = MyDynamicMplCanvas()
		#底部
		self.__textEdit = QTextEdit(self)
		self.widget5 = MyStaticMplCanvas()
		self.widget6 = MyStaticMplCanvas()
		

		#设置顶部四个图的分割布局
		# Qt.Vertical 垂直   Qt.Horizontal 水平
		splitterTop_H = QSplitter(Qt.Horizontal)
		splitterTop_H.setSizes([200, 400])
		splitterTop_H.addWidget(self.widget1)
		splitterTop_H.addWidget(self.widget2)
		splitterTop_H.addWidget(self.widget3)
		splitterTop_H.addWidget(self.widget4)

		#设置底部界面两个图的分割布局
		splitterBottom_H = QSplitter(Qt.Horizontal)
		tmpStr = "VOC 15PPm\nCO 10ppm\nNO2 3ppm\nHCHO 3ppm"
		self.__textEdit.setText(tmpStr)
		self.__textEdit.setAlignment(Qt.AlignHCenter)
		self.__textEdit.setAlignment(Qt.AlignHCenter)
		splitterBottom_H.addWidget(self.__textEdit)
		splitterBottom_H.addWidget(self.widget5)
		splitterBottom_H.addWidget(self.widget6)
		
		#创建主的分割布局，并将顶部和底部的布局添加到其中
		splitterMain_V = QSplitter(Qt.Vertical)
		splitterMain_V.addWidget(splitterTop_H)
		splitterMain_V.addWidget(splitterBottom_H)
		
		#创建顶部按钮控件

		btn1 = QtWidgets.QPushButton()
		btn1.setText("BTN1")
		btn1.clicked.connect(self.btn1_clicked)
		#btn1.setFont(QFont("times",12,QFont.Bold))
		#btn1.setFixedSize(160,80)
		btn1.adjustSize()

		btn2 = QtWidgets.QPushButton()
		btn2.setText("BTN2")
		btn2.clicked.connect(self.btn2_clicked)
		btn2.adjustSize()

		btn3 = QtWidgets.QPushButton()
		btn3.setText("BTN3")
		btn3.clicked.connect(self.btn2_clicked)
		btn3.adjustSize()

		btn4 = QtWidgets.QPushButton()
		btn4.setText("BTN4")
		btn4.clicked.connect(self.btn4_clicked)
		btn4.adjustSize()

		menuTopWidget = QtWidgets.QWidget()
		menuTopWidget.adjustSize()
		menuTopWidget.setMaximumWidth(200)

		menuTopLayout_V = QVBoxLayout(menuTopWidget)
		menuTopLayout_V.addStretch()
		menuTopLayout_H = QHBoxLayout()
		menuTopLayout_H.addWidget(btn2, 0, Qt.AlignCenter)
		menuTopLayout_H.addWidget(btn3, 0, Qt.AlignCenter)
		menuTopLayout_V.addWidget(btn1, 0, Qt.AlignCenter)
		menuTopLayout_V.addLayout(menuTopLayout_H)
		menuTopLayout_V.addWidget(btn4, 0, Qt.AlignCenter)
		menuTopLayout_V.addStretch()
		
		#创建底部widget
		
		btn5 = QtWidgets.QPushButton()
		btn5.setText("BTN5")
		btn5.clicked.connect(self.btn5_clicked)
		btn5.adjustSize()

		btn6 = QtWidgets.QPushButton()
		btn6.setText("BTN6")
		btn6.clicked.connect(self.btn6_clicked)
		btn6.adjustSize()

		btn7 = QtWidgets.QPushButton()
		btn7.setText("BTN7")
		btn7.clicked.connect(self.btn7_clicked)
		btn7.adjustSize()

		menuBottomWidget = QtWidgets.QWidget()
		menuBottomWidget.adjustSize()

		menuBottomWidgetLayout_V = QVBoxLayout(menuBottomWidget)
		menuBottomWidgetLayout_H = QHBoxLayout()
		menuBottomWidgetLayout_H.addWidget(btn6, 0, Qt.AlignCenter)
		menuBottomWidgetLayout_H.addWidget(btn7, 0, Qt.AlignCenter)
		menuBottomWidgetLayout_V.addWidget(btn5, 0, Qt.AlignCenter)
		menuBottomWidgetLayout_V.addLayout(menuBottomWidgetLayout_H)
		menuBottomWidgetLayout_V.addStretch()


		#将相关部件添加到，splitter_menu中
		splitterMenu_V = QSplitter(Qt.Vertical)
		splitterMenu_V.addWidget(menuTopWidget)
		splitterMenu_V.addWidget(menuBottomWidget)

		#将相关部件添加到mainWidget中
		self.mainWidget.setLayout(self.hBox)
		self.hBox.addWidget(splitterMenu_V)
		self.hBox.addWidget(splitterMain_V)

	

	#弹出提示信息
	def btn5_clicked(self):
		pass
	
	def btn6_clicked(self):
		pass
	
	def btn7_clicked(self):
		pass


	#获取测试数据路径
	def btn1_clicked(self):
		pass

	#获取模型文件路径
	def btn2_clicked(self):
		
		pass
	
	#绘制图形
	def btn4_clicked(self):
		pass
		

if __name__ == '__main__':
	app = QApplication(sys.argv)
	demo = MainWindow()
	demo.show()
	sys.exit(app.exec_())

