from lector import leer_mapa
from PyQt4 import QtGui
from gui.gui import GrillaSimulacion
from random import expovariate, uniform, randint, choice
from itertools import permutations
from edificios import Casa, Hospital, Cuartel, Comisaria


SIMETRIA = {'derecha': [0, False], 'izquierda': [0, True],
            'arriba': [270, False], 'abajo': [90, False]}


class Auto:

    def __init__(self, sentido):
        self.velocidad = uniform(0.5, 1)
        self.taxi = True if randint(0, 9) > 7 else False
        self.ultimo_mov = 0
        self.sentido = sentido


class Vacio:

    def __repr__(self):
        return ' ◯'  # ●


class Calle:

    def __init__(self, sentido):
        self.sentido = sentido
        self.auto = None
        self.semaforo = [False, 'horizontal']
        self.posicion = (0, 0)

    def __repr__(self):
        if self.semaforo[0]:
            return ' s'
        if self.auto:
            return ' a'
        if self.sentido == 'arriba':
            return ' ↑'
        elif self.sentido == 'abajo':
            return ' ↓'
        elif self.sentido == 'derecha':
            return ' →'
        elif self.sentido == 'izquierda':
            return ' ←'


class Ciudad:

    def __init__(self, interface, rows, cols, calles, casas, vacios):
        self.matrix = [[Vacio() for i in range(cols)] for j in range(rows)]
        self.interface = interface
        self.tiempo = 0
        self.rows = rows
        self.cols = cols
        self.semaforos = []
        self.casas = []
        self.calles = []
        self.autos = []
        self.agregar_calles(calles)
        self.agregar_casas(casas)
        self.agregar_vacios(vacios)
        self.obtener_semaforos()

    @property
    def max_autos(self):
        c = (sum(1 for j in i if isinstance(j, Calle)) for i in self.matrix)
        return sum(c) // 4

    def marcar_semaforo(self, calle):
        x, y = calle.posicion
        if calle.sentido == 'abajo' or calle.sentido == 'arriba':
            colindantes = [(x, y - 1), (x, y + 1), (x, y - 2), (x, y + 2)]
            for i, j in colindantes:
                if (0 <= i < self.rows and 0 <= j < self.cols and
                        isinstance(self.matrix[i][j], Calle)):
                    if self.matrix[i][j].sentido != calle.sentido:
                        calle.semaforo[0] = True
                        self.semaforos.append(calle)
        elif calle.sentido == 'derecha' or calle.sentido == 'izquierda':
            colindantes = [(x - 1, y), (x + 1, y), (x - 2, y), (x + 2, y)]
            for i, j in colindantes:
                if (0 <= i < self.rows and 0 <= j < self.cols and
                        isinstance(self.matrix[i][j], Calle)):
                    if self.matrix[i][j].sentido != calle.sentido:
                        calle.semaforo[0] = True
                        self.semaforos.append(calle)

    def obtener_semaforos(self):
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[0])):
                if type(self.matrix[i][j]) == Calle:
                    calle = self.matrix[i][j]
                    self.marcar_semaforo(calle)

    def agregar_calles(self, calles):
        self.calles = calles
        for calle in calles:
            x, y = calle['posicion']
            objeto_calle = Calle(calle['sentido'])
            objeto_calle.posicion = (x - 1, y - 1)
            self.matrix[x - 1][y - 1] = objeto_calle
            self.interface.agregar_calle(x, y)
        self.calles.append(objeto_calle)

    def agregar_casas(self, casas):
        self.casas = casas
        for casa in casas:
            x, y = casa['posicion']
            objeto_casa = Casa(casa['material'], casa['rango_robos'])
            self.matrix[x - 1][y - 1] = objeto_casa
            self.interface.agregar_casa(x, y)
        self.casas.append(objeto_casa)

    def agregar_vacios(self, vacios):
        self.vacios = vacios

    def agregar_autos(self):
        for i in range(1):
            pos = (0, 0)  # range(randint(self.max_autos // 2, self.max_autos))
            while not isinstance(self.matrix[pos[0]][pos[1]], Calle):
                pos = (randint(0, self.interface.rows - 1),
                       randint(0, self.interface.cols - 1))
            sentido = self.matrix[pos[0]][pos[1]].sentido
            auto = Auto(sentido)
            if sentido == 'derecha':
                # se intenta poner en la pista derecha para los 4 casos
                nx, ny = pos[0] + 1, pos[1]
                if (nx < self.rows and isinstance(self.matrix[nx][ny], Calle)):
                    if self.matrix[nx][ny].sentido == sentido:
                        pos = nx, ny
            elif sentido == 'izquierda':
                nx, ny = pos[0] - 1, pos[1]
                if (nx < self.rows and isinstance(self.matrix[nx][ny], Calle)):
                    if self.matrix[nx][ny].sentido == sentido:
                        pos = nx, ny
            elif sentido == 'arriba':
                nx, ny = pos[0], pos[1] + 1
                if (ny < self.cols and isinstance(self.matrix[nx][ny], Calle)):
                    if self.matrix[nx][ny].sentido == sentido:
                        pos = nx, ny
            else:
                nx, ny = pos[0], pos[1] - 1
                if (ny < self.cols and isinstance(self.matrix[nx][ny], Calle)):
                    if self.matrix[nx][ny].sentido == sentido:
                        pos = nx, ny
            grados, reflect = SIMETRIA[sentido]
            if (self.matrix[pos[0]][pos[1]].semaforo[0] or
                    self.matrix[pos[0]][pos[1]].auto is not None):
                # como las posiciones son generadas aleatoriamente
                # puede caer o no en semaforos indistintamente, por lo que
                # así se genera un número de autos aleatorio <= al maximo
                # ya que no se ponen autos en un principio en los semaforos
                continue  # ni donde haya un auto previamente
            auto.posicion = pos
            self.matrix[pos[0]][pos[1]].auto = auto
            auto.grados = grados
            auto.reflect = reflect
            self.interface.agregar_auto(pos[0] + 1, pos[1] + 1,
                                        grados, reflect)
            # self.interface.tiempo_intervalo = 1
            # self.interface.actualizar()
            self.autos.append(auto)

    def agregar_estacion(self, estacion, posicion):
        dicc = {'cuartel': self.interface.agregar_cuartel_bomberos,
                'hospital': self.interface.agregar_hospital,
                'comisaria': self.interface.agregar_comisaria,
                'vacio': lambda x, y: x}
        dicc[estacion.__class__.__name__.lower()](*posicion)

    def moverse_si_puede(self, auto, npos, sentido):
        direccion = 'horizontal' if sentido in ['derecha',
                                                'izquierda'] else 'vertical'
        sentido_original = sentido
        x, y = auto.posicion
        nx, ny = npos
        if (0 <= nx < self.rows and 0 <= ny < self.cols and
                isinstance(self.matrix[nx][ny], Calle)):
            semaforo = self.matrix[nx][ny].semaforo
            if semaforo[0] and semaforo[1] != direccion:
                # print('para por semaforo', x, y)
                return False
            elif self.matrix[nx][ny].auto is not None:
                # print('hay auto adelante', x, y)
                return False
            elif semaforo[0]:
                if self.matrix[auto.posicion[0]][auto.posicion[1]].semaforo[0]:
                    factor = 2
                else:
                    factor = 3
                tiempo_dos_cuadrados = (1 / auto.velocidad) * factor
                tiempo_cambio_sem = (self.tiempo // 20) * 20 + 20
                # print(tiempo_cambio_sem, self.tiempo + tiempo_dos_cuadrados)
                if self.tiempo + tiempo_dos_cuadrados > tiempo_cambio_sem:
                    # print('no alcanzo a cruzar')
                    return False
                else:
                    # se simula movimiento de portal en los semaf
                    while True:
                        if sentido == 'derecha':
                            nnx, nny = nx, ny + 2
                        elif sentido == 'izquierda':
                            nnx, nny = nx, ny - 2
                        elif sentido == 'arriba':
                            nnx, nny = nx - 2, ny
                        elif sentido == 'abajo':
                            nnx, nny = nx + 2, ny
                        if (0 <= nnx < self.rows and 0 <= nny < self.cols and
                                isinstance(self.matrix[nnx][nny], Calle)):
                            if self.matrix[nnx][nny].auto is None:
                                nx, ny = nnx, nny
                            else:
                                nx, ny = x, y
                            break
                        else:
                            sentido = choice(
                                ['derecha', 'izquierda', 'arriba', 'abajo'])
            else:
                # print('sigue', x, y)
                self.matrix[nx][ny].auto = auto
                self.matrix[x][y].auto = None
                auto.ultimo_mov = self.tiempo
                self.interface.quitar_imagen(x + 1, y + 1)
                if sentido_original == sentido:
                    grados = auto.grados
                    reflect = auto.reflect
                else:
                    grados, reflect = SIMETRIA[sentido]
                self.interface.agregar_auto(
                    nx + 1, ny + 1, grados, reflect)
                self.interface.actualizar()
                return True

    def mover_autos(self):
        for auto in self.autos:
            x, y = auto.posicion
            if self.tiempo - auto.ultimo_mov >= 1 / auto.velocidad:
                if auto.sentido == 'arriba':
                    self.moverse_si_puede(auto, (x - 1, y), 'arriba')
                elif auto.sentido == 'abajo':
                    self.moverse_si_puede(auto, (x + 1, y), 'abajo')
                elif auto.sentido == 'derecha':
                    self.moverse_si_puede(auto, (x, y + 1), 'derecha')
                elif auto.sentido == 'izquierda':
                    self.moverse_si_puede(auto, (x, y - 1), 'izquierda')

    def cambiar_semaforos(self, direccion):
        for calle in self.semaforos:
            calle.semaforo[1] = direccion

    def posibles(self):
        edificios = [Hospital(), Cuartel(), Comisaria(), Vacio()]
        combinaciones = list(permutations(edificios))
        for i in combinaciones[:1]:
            for l in self.vacios:
                self.interface.quitar_imagen(*l['posicion'])
            for j, k in zip(i, self.vacios):
                posicion = k['posicion']
                self.agregar_estacion(j, posicion)
            self.simular(50)

    def simular(self, veces):
        self.interface.tiempo_intervalo = 1
        for i in range(100):
            tiempo = uniform(0.5, 1)
            self.tiempo += tiempo
            self.mover_autos()
            if int(self.tiempo) % 20 == 0:
                # print('->', self.tiempo, 'cambioo')
                if (int(self.tiempo) / 20) % 2 == 0:
                    self.cambiar_semaforos('vertical')
                else:
                    self.cambiar_semaforos('horizontal')
            # self.interface.actualizar()

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
    city = Ciudad(interfaz, datos[0][0], datos[0][1],
                  datos[1], datos[3], datos[2])
    print(city.max_autos)
    city.agregar_autos()
    city.interface.actualizar()
    print([i.posicion for i in city.autos])
    city.interface.show()
    print(len(city.autos))
    # print(city)
    city.interface.tiempo_intervalo = 0.5
    city.posibles()
    # print(city)
    # city.interface.actualizar()
    app.exec_()
