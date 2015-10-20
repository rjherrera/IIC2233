import sys
from PyQt4 import QtGui, QtCore
from backend import Partida
from time import sleep


class Buscaminas(QtGui.QWidget):

    def __init__(self, n, minas):  # con "n" se genera una matriz de nxn
        super(Buscaminas, self).__init__()
        self.n = n
        self.minas = minas
        self.partida = Partida(n, minas)
        ":::COMPLETAR:::"
        self.ya_gano = False
        self.initUI()

    def initUI(self):
        grilla = QtGui.QGridLayout()
        self.setLayout(grilla)
        for i in range(self.n):
            for j in range(self.n):
                boton = QtGui.QPushButton('')
                boton.pos = (i, j)
                # boton.setText(self.apretar_boton(boton.pos))
                boton.setFixedSize(50, 50)
                grilla.addWidget(boton, i, j)
                boton.clicked.connect(self.buttonClickedLeft)
        self.label = QtGui.QLabel('', self)
        grilla.addWidget(self.label, self.n, 0, self.n, self.n)
        self.setWindowTitle('Vu Chef')
        self.show()

    def buttonClickedLeft(self):
        boton = self.sender()
        if self.perdedor():
            self.notificar('Ya perdiste, no puedes seguir jugando')
        else:
            valor = self.apretar_boton(boton.pos)
            if self.ganador() and not self.ya_gano:
                self.notificar('Ganaste! Felicitaciones')
                boton.setText(valor)
                self.ya_gano = True
            elif not self.ya_gano:
                if boton.text() == '':
                    boton.setText(valor)
                if valor == 'X':
                    self.notificar('Moriste! Pisaste una mina')
                else:
                    self.notificar('Sigues! Pisaste un lugar seguro')
            else:
                self.notificar('Ya ganaste! Puedes retirarte')

    def apretar_boton(self, posicion):  # Posición como una tupla (x, y)
        "Esta funcion devuelve la cantidad de minas alrededor de un espacio"
        "No tiene ninguna relación con lo que sucederá en la UI"
        boton = self.partida.botones[posicion]
        return self.partida.clickear(boton)

    def notificar(self, mensaje):
        ":::COMPLETAR:::"
        "Debe notificar a traves de un label cuando muera o sobreviva"
        self.label.setText(mensaje)

    def ganador(self):
        botones = (j for i, j in self.partida.botones.items())
        seguros = list(filter(lambda x: not x.mina and x.clickeado, botones))
        return len(seguros) == self.n ** 2 - self.minas

    def perdedor(self):
        botones = (j for i, j in self.partida.botones.items())
        minas = list(filter(lambda x: x.mina and x.clickeado, botones))
        return len(minas) != 0


if __name__ == '__main__':
        app = QtGui.QApplication(sys.argv)
        ex = Buscaminas(5, 10)
        sys.exit(app.exec_())
