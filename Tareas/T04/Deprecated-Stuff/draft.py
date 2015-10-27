from lector import leer_mapa
from PyQt4 import QtGui
from gui.gui import GrillaSimulacion
from random import expovariate, uniform, randint
from itertools import permutations
from edificios import Casa, Hospital, Cuartel, Comisaria
from time import sleep
import sys


class Auto:

    def __init__(self):
        self.velocidad = uniform(0.5, 1)
        self.taxi = True if randint(0, 9) >= 8 else False

    def __repr__(self):
        if self.sentido == 'arriba':
            return ' ▲'
        elif self.sentido == 'abajo':
            return ' ▼'
        elif self.sentido == 'derecha':
            return ' ►'
        elif self.sentido == 'izquierda':
            return ' ◄'


class Vacio:

    def __repr__(self):
        return ' ◯'  # ●


class Calle:

    def __init__(self, sentido):
        self.sentido = sentido
        self.auto = None

    def __repr__(self):
        if self.sentido == 'arriba':
            return ' ↑'
        elif self.sentido == 'abajo':
            return ' ↓'
        elif self.sentido == 'derecha':
            return ' →'
        elif self.sentido == 'izquierda':
            return ' ←'


class Ciudad:

    def __init__(self, interface, rows, cols):
        self.matrix = [[Vacio() for i in range(cols)] for j in range(rows)]
        self.interface = interface
        self.tiempo = 0

    @property
    def max_autos(self):
        c = (sum(1 for j in i if isinstance(j, Calle)) for i in self.matrix)
        return sum(c) // 4

    def agregar_calles(self, calles):
        self.calles = calles
        for calle in calles:
            x, y = calle['posicion']
            self.matrix[x - 1][y - 1] = Calle(calle['sentido'])
            self.interface.agregar_calle(x, y)

    def agregar_casas(self, casas):
        self.casas = casas
        for casa in casas:
            x, y = casa['posicion']
            self.matrix[x - 1][y - 1] = Casa(
                casa['material'], casa['rango_robos'])
            self.interface.agregar_casa(x, y)

    def agregar_vacios(self, vacios):
        self.vacios = vacios

    def agregar_autos(self):
        for i in range(randint(self.max_autos // 2, self.max_autos)):
            pos = (0, 0)
            while not isinstance(self.matrix[pos[0]][pos[1]], Calle):
                pos = (randint(0, self.interface.rows-1),
                       randint(0, self.interface.cols-1))
            self.matrix[pos[0]][pos[1]].auto = Auto()
            direccion = self.matrix[pos[0]][pos[1]].sentido
            reflect = False
            if direccion == 'derecha':
                grados = 0
            elif direccion == 'izquierda':
                grados = 0
                reflect = True
            elif direccion == 'arriba':
                grados = 270
            else:
                grados = 90
            self.interface.agregar_auto(pos[0]+1, pos[1]+1, grados, reflect)

    def agregar_estacion(self, estacion, posicion):
        dicc = {'cuartel': self.interface.agregar_cuartel_bomberos,
                'hospital': self.interface.agregar_hospital,
                'comisaria': self.interface.agregar_comisaria,
                'vacio': lambda x, y: x}
        dicc[estacion.__class__.__name__.lower()](*posicion)

    def posibles(self):
        edificios = [Hospital(), Cuartel(), Comisaria(), Vacio()]
        combinaciones = list(permutations(edificios))
        for i in combinaciones:
            for l in self.vacios:
                self.interface.quitar_imagen(*l['posicion'])
            for j, k in zip(i, self.vacios):
                posicion = k['posicion']
                self.agregar_estacion(j, posicion)
            self.simular()

    def simular(self):
        self.interface.actualizar()

    def __str__(self):
        string = '⚹  ' + ' '.join(
            str(i).ljust(2) for i in range(1, len(self.matrix[0]) + 1)) + '\n'
        for i, j in zip(self.matrix, range(1, len(self.matrix) + 1)):
            string += str(j).ljust(2) + ' '.join(str(j) for j in i) + '\n'
        return string[:-1]

if __name__ == '__main__':
    datos = leer_mapa('mapa fix.txt')
    app = QtGui.QApplication([])
    interfaz = GrillaSimulacion(app, *datos[0])
    city = Ciudad(interfaz, *datos[0])
    city.agregar_calles(datos[1])
    city.agregar_casas(datos[3])
    city.agregar_vacios(datos[2])
    print(city.max_autos)
    city.agregar_autos()
    city.interface.actualizar()
    city.interface.show()
    # print(city)
    city.interface.tiempo_intervalo = 0.5
    city.posibles()
    # city.interface.actualizar()
    app.exec_()
