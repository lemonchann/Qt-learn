from PyQt5.QtCore import QDateTime, QTimer, Qt, pyqtSlot
from PyQt5.QtWidgets import QLCDNumber, QApplication
from PyQt5.QtGui import QCursor
import sys


class Maindow(QLCDNumber):
    def __init__(self):
        super(Maindow, self).__init__()
        timer = QTimer(self)
        timer.timeout.connect(self.__timeout)
        timer.start(100)
        self.setWindowFlag(Qt.FramelessWindowHint)

    def __timeout(self):
        currentTime = QDateTime()
        hms = currentTime.time()
        self.display(hms.toString("hh:mm:ss"))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    @pyqtSlot()
    def on_pushButton_clicked(self):
        """
        关闭窗口
        """
        self.close()

    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        """
        最小化窗口
        """
        self.showMinimized()


if __name__ == "__main__":

    app = QApplication(sys.argv)
    MW = Maindow()
    MW.show()
    sys.exit(app.exec_())
