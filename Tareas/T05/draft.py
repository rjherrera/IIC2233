from PyQt4 import QtGui, uic

form = uic.loadUiType("zombies.ui")


class MainWindow(form[0], form[1]):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        pixmap = QtGui.QPixmap('logo_argentum.png')
        self.label.setPixmap(pixmap)
        self.label.resize(self.label.sizeHint())
        # self.label_15.move(90, 0)
        # self.label_16.setScaledContents(True)
        # self.label_16.setPixmap(QtGui.QPixmap('logo_hexa.png'))
        # self.label_16.resize(100, 30)
        # self.label_14.move(105, 68)
        # # aporte mensual
        # self.lineEdit.textChanged.connect(self.calcular)
        # self.lineEdit_2.textChanged.connect(self.calcular)
        # # años
        # self.lineEdit_4.textChanged.connect(self.calcular)
        # self.lineEdit_5.textChanged.connect(self.calcular)
        # self.lineEdit_6.textChanged.connect(self.calcular)
        # # combobox
        # self.comboBox.currentIndexChanged.connect(self.calcular)
        # # Completar la creación de la interfaz #

if __name__ == '__main__':
    app = QtGui.QApplication([])
    form = MainWindow()
    form.show()
    app.exec_()
