import sys
from MyMplCanvas import MyStaticMplCanvas
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QTextEdit, QFormLayout, QSizePolicy, QAction
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QComboBox, QMessageBox, QLineEdit, QMainWindow, QDockWidget
from PyQt5.QtGui import QImage, QIcon, QPixmap
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()
		layout = QVBoxLayout()
		self.setDockNestingEnabled(True)

		dock1 = QDockWidget("dock1")
		dock1.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea | Qt.BottomDockWidgetArea | Qt.TopDockWidgetArea)
		dock1_widget = MyStaticMplCanvas()
		dock1.setWidget(dock1_widget)
		self.addDockWidget(Qt.RightDockWidgetArea, dock1)

		dock2 = QDockWidget("dock2")
		dock2.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea | Qt.BottomDockWidgetArea | Qt.TopDockWidgetArea)
		dock2_widget = MyStaticMplCanvas()
		dock2.setWidget(dock2_widget)
		self.addDockWidget(Qt.RightDockWidgetArea, dock2)

		dock3 = QDockWidget("dock3")
		dock3.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea | Qt.BottomDockWidgetArea | Qt.TopDockWidgetArea)
		dock3_widget = MyStaticMplCanvas()
		dock3.setWidget(dock3_widget)
		self.addDockWidget(Qt.RightDockWidgetArea, dock3)

		dock4 = QDockWidget("dock4")
		dock4_widget = MyStaticMplCanvas()
		dock4.setWidget(dock4_widget)
		self.addDockWidget(Qt.RightDockWidgetArea, dock4)

		dock5 = QDockWidget("dock5")
		dock5_widget = MyStaticMplCanvas()
		dock5.setWidget(dock5_widget)
		self.addDockWidget(Qt.RightDockWidgetArea, dock5)

		dock6 = QDockWidget("dock6")
		dock6_widget = MyStaticMplCanvas()
		dock6.setWidget(dock6_widget)
		self.addDockWidget(Qt.RightDockWidgetArea, dock6)

		btn1 = QPushButton("btn1")
		btn2 = QPushButton("btn2")
		cenWidget = QWidget()
		
		cenWidget.setMaximumWidth(200)
		cenWidget.setLayout(layout)
		self.setCentralWidget(cenWidget)
		layout.addWidget(btn1)
		layout.addWidget(btn2)
				

if __name__ == "__main__":
	app = QApplication(sys.argv)
	MW = MainWindow()
	MW.show()
	sys.exit(app.exec_())
