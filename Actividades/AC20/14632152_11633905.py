from PyQt4 import QtGui, uic
from calc_financiero import calcular_jub

form = uic.loadUiType("hexa.ui")


class MainWindow(form[0], form[1]):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        pixmap = QtGui.QPixmap('logo_argentum.png')
        self.label_15.setPixmap(pixmap)
        self.label_15.resize(self.label_15.sizeHint())
        self.label_15.move(90, 0)
        self.label_16.setScaledContents(True)
        self.label_16.setPixmap(QtGui.QPixmap('logo_hexa.png'))
        self.label_16.resize(100, 30)
        self.label_14.move(105, 68)
        # aporte mensual
        self.lineEdit.textChanged.connect(self.calcular)
        self.lineEdit_2.textChanged.connect(self.calcular)
        # años
        self.lineEdit_4.textChanged.connect(self.calcular)
        self.lineEdit_5.textChanged.connect(self.calcular)
        self.lineEdit_6.textChanged.connect(self.calcular)
        # combobox
        self.comboBox.currentIndexChanged.connect(self.calcular)
        # Completar la creación de la interfaz #

    def calcular(self):
        """ Completar esta función para calcular los cambios de los datos
        en tiempo real según el input del usuario. """
        # aporte mensual
        ingreso = self.lineEdit
        porcentaje = self.lineEdit_2
        error = False
        if ingreso.text() and porcentaje.text():
            try:
                porcentaje_valor = float(porcentaje.text())
                res = int(ingreso.text()) * porcentaje_valor / 100
                if not 0 <= porcentaje_valor <= 100:
                    raise ValueError
                self.label_2.setText('$%f' % res)
                self.statusbar.showMessage('')
                error = False
            except:
                if not error:
                    self.statusbar.showMessage(
                        'Ingreso y/o porcentaje inválidos.')
                    error = True
        # años de pension
        edad_jubilacion = self.lineEdit_5
        esperanza = self.lineEdit_6
        if edad_jubilacion.text() and esperanza.text():
            try:
                res = int(esperanza.text()) - int(edad_jubilacion.text())
                self.label_5.setText('%d' % res)
                self.statusbar.showMessage('')
                error = False
            except:
                if not error:
                    self.statusbar.showMessage('Edades inválidas.')
                    error = True
        # calculo final
        edad_actual = self.lineEdit_4
        seleccion = self.comboBox.itemText(self.comboBox.currentIndex())
        if (ingreso.text() and porcentaje.text() and edad_actual.text() and
                edad_jubilacion.text() and esperanza.text() and seleccion):
            try:
                res = calcular_jub(int(ingreso.text()),
                                   float(porcentaje.text()),
                                   int(edad_actual.text()),
                                   int(edad_jubilacion.text()),
                                   int(esperanza.text()),
                                   seleccion)
                self.label_13.setText(res)
                self.statusbar.showMessage('')
                error = False
            except:
                if not error:
                    self.statusbar.showMessage(
                        'Error en los datos ingresados.')
                    error = True


if __name__ == '__main__':
    app = QtGui.QApplication([])
    form = MainWindow()
    form.show()
    app.exec_()
