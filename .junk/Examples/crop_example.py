import sys
from PyQt5 import QtGui, QtCore, QtWidgets

class QExampleLabel (QtWidgets.QLabel):
    def __init__(self, parentQWidget = None):
        super(QExampleLabel, self).__init__(parentQWidget)
        self.initUI()

    def initUI (self):
        self.setPixmap(QtGui.QPixmap('input.jpg'))

    def mousePressEvent (self, eventQMouseEvent):
        self.originQPoint = eventQMouseEvent.pos()
        self.currentQRubberBand = QtWidgets.QRubberBand(QtWidgets.QRubberBand.Rectangle, self)
        self.currentQRubberBand.setGeometry(QtCore.QRect(self.originQPoint, QtCore.QSize()))
        self.currentQRubberBand.show()

    def mouseMoveEvent (self, eventQMouseEvent):
        self.currentQRubberBand.setGeometry(QtCore.QRect(self.originQPoint, eventQMouseEvent.pos()).normalized())

    def mouseReleaseEvent (self, eventQMouseEvent):
        self.currentQRubberBand.hide()
        currentQRect = self.currentQRubberBand.geometry()
        self.currentQRubberBand.deleteLater()
        cropQPixmap = self.pixmap().copy(currentQRect)
        cropQPixmap.save('output.jpg')

if __name__ == '__main__':
    myQApplication = QtWidgets.QApplication(sys.argv)
    myQExampleLabel = QExampleLabel()
    myQExampleLabel.show()
    sys.exit(myQApplication.exec_())