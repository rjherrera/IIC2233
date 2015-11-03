from PyQt4 import QtCore, QtGui

class Window(QtGui.QWidget):
    cursorMove = QtCore.pyqtSignal(object)

    def __init__(self):
        super(Window, self).__init__()
        self.cursorMove.connect(self.handleCursorMove)
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.pollCursor)
        self.timer.start()
        self.cursor = None

    def pollCursor(self):
        pos = QtGui.QCursor.pos()
        if pos != self.cursor:
            self.cursor = pos
            self.cursorMove.emit(pos)

    def handleCursorMove(self, pos):
        print(pos)

if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.setGeometry(500, 500, 200, 200)
    window.show()
    sys.exit(app.exec_())