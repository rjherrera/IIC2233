from lector import leer_mapa
from PyQt4 import QtGui
from gui.gui import GrillaSimulacion
from random import expovariate, uniform, randint, choice
from itertools import permutations
from edificios import Casa, Hospital, Cuartel, Comisaria
from vehiculos import Auto, Ambulancia, Carro, Policia


SIMETRIA = {'derecha': [0, False], 'izquierda': [0, True],
            'arriba': [270, False], 'abajo': [90, False]}
T_SEMAFORO = 20
T_HORIZONTE = 14 * 24  # * 3600


class Vacio:

    pass


class Calle:

    def __init__(self, sentido):
        self.sentido = sentido
        self.auto = None
        self.semaforo = [False, 'horizontal']
        self.posicion = (0, 0)


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

    @property
    def pesos_casas(self):
        return sum(i.peso for i in self.casas)

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
        for i in range(self.max_autos):
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

    def obtener_post_interseccion(self, auto):
        sentido = auto.sentido
        x, y = auto.posicion
        posibles = []
        if sentido == 'derecha':
            aux = []
            aux.append([x, y + 3, 'derecha'])
            aux.append([x + 1, y + 1, 'abajo'])
            aux.append([x - 2, y + 2, 'arriba'])
            for i, j, k in aux:
                if (0 <= i < self.rows and 0 <= j < self.cols and
                        isinstance(self.matrix[i][j], Calle)):
                    if k == self.matrix[i][j].sentido:
                        posibles.append([i, j, self.matrix[i][j].sentido])
        elif sentido == 'izquierda':
            aux = []
            aux.append([x, y - 3, 'izquierda'])
            aux.append([x + 2, y - 2, 'abajo'])
            aux.append([x - 1, y - 1, 'arriba'])
            for i, j, k in aux:
                if (0 <= i < self.rows and 0 <= j < self.cols and
                        isinstance(self.matrix[i][j], Calle)):
                    if k == self.matrix[i][j].sentido:
                        posibles.append([i, j, self.matrix[i][j].sentido])
        elif sentido == 'arriba':
            aux = []
            aux.append([x - 3, y, 'arriba'])
            aux.append([x - 1, y + 1, 'derecha'])
            aux.append([x - 2, y - 2, 'izquierda'])
            for i, j, k in aux:
                if (0 <= i < self.rows and 0 <= j < self.cols and
                        isinstance(self.matrix[i][j], Calle)):
                    if k == self.matrix[i][j].sentido:
                        posibles.append([i, j, self.matrix[i][j].sentido])
        elif sentido == 'abajo':
            aux = []
            aux.append([x + 3, y, 'abajo'])
            aux.append([x + 2, y + 2, 'derecha'])
            aux.append([x + 1, y - 1, 'izquierda'])
            for i, j, k in aux:
                if (0 <= i < self.rows and 0 <= j < self.cols and
                        isinstance(self.matrix[i][j], Calle)):
                    if k == self.matrix[i][j].sentido:
                        posibles.append([i, j, self.matrix[i][j].sentido])
        pos = choice(posibles)
        return pos

    def mover_auto_entrada(self, auto):
        while True:
            i = randint(0, self.rows + self.cols - 1)
            pos = (i, 0)
            if i > self.rows - 1:
                pos = (0, i - self.rows)
            if (isinstance(self.matrix[pos[0]][pos[1]], Calle) and
                    self.matrix[pos[0]][pos[1]].auto is None):
                calle = self.matrix[pos[0]][pos[1]]
                if calle.sentido in ['derecha', 'abajo']:
                    if calle.sentido == 'derecha':
                        nx, ny = pos[0] + 1, pos[1]
                        if (nx < self.rows and isinstance(self.matrix[nx][ny], Calle)):
                            if self.matrix[nx][ny].sentido == calle.sentido:
                                pos = nx, ny
                    else:
                        nx, ny = pos[0], pos[1] - 1
                        if (ny < self.cols and isinstance(self.matrix[nx][ny], Calle)):
                            if self.matrix[nx][ny].sentido == calle.sentido:
                                pos = nx, ny
                    auto.sentido = calle.sentido
                    auto.posicion = pos
                    calle.auto = auto
                    # print(calle.sentido, pos)
                    sime = SIMETRIA[calle.sentido]
                    auto.grados, auto.reflect = sime
                    self.interface.agregar_auto(pos[0] + 1, pos[1] + 1, *sime)
                    return

    def moverse_si_puede(self, auto, npos, sentido):
        x, y = auto.posicion
        nx, ny = npos
        direc = 'horizontal' if sentido in ['derecha',
                                            'izquierda'] else 'vertical'
        if 0 <= nx < self.rows and 0 <= ny < self.cols:
            if isinstance(self.matrix[nx][ny], Calle):
                calle_sig = self.matrix[nx][ny]
                if calle_sig.semaforo[0] and calle_sig.semaforo[1] != direc:
                    # print('semaforo en rojo')
                    return False
                elif calle_sig.semaforo[0]:
                    # print('INTERSECCION - DEBO SEGUIR O DOBLAR - PORTAL')
                    data = self.obtener_post_interseccion(auto)
                    if data != (-1, -1, ''):
                        nx, ny, sentido = data
                    auto.grados, auto.reflect = SIMETRIA[sentido]
                if calle_sig.auto is not None:
                    # print('habia auto')
                    return False
                # print('ME MUEVO A', x, y)
                self.interface.quitar_imagen(x + 1, y + 1)
                self.matrix[x][y].auto = None
                self.matrix[nx][ny].auto = auto
                auto.sentido = sentido
                self.interface.agregar_auto(nx + 1, ny + 1, *SIMETRIA[sentido])
                auto.posicion = nx, ny
                self.interface.actualizar()
        else:
            # print('SALGO', x, y, nx, ny, direc)
            self.interface.quitar_imagen(x + 1, y + 1)
            self.matrix[x][y].auto = None
            self.mover_auto_entrada(auto)
            self.interface.actualizar()

    def mover_autos(self):
        # print(self.semaforos[0].semaforo[1])
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

    def generar_incendios(self):
        tiempo = expovariate(1 / (10 * 60))
        if self.tiempo >= tiempo:
            for casa in self.casas:
                casa.prob = casa.peso / self.pesos_casas
            self.casas.sort(lambda x: x.prob)
            # continuaría

    def posibles(self):
        edificios = [Hospital(), Cuartel(), Comisaria(), Vacio()]
        combinaciones = list(permutations(edificios))
        for i in combinaciones:
            for l in self.vacios:
                self.interface.quitar_imagen(*l['posicion'])
            for j, k in zip(i, self.vacios):
                posicion = k['posicion']
                self.agregar_estacion(j, posicion)
            self.simular(50)

    def obtener_estadisticas(self):
        # t_b = sum(i.tiempo for i in self.bomberos) / len(self.bomberos)
        pass

    def simular(self, veces):
        self.interface.tiempo_intervalo = 0.2
        for i in range(veces):
            # print(len(self.autos))
            while self.tiempo < T_HORIZONTE:
                tiempo = uniform(0.5, 1)
                self.tiempo += tiempo
                self.mover_autos()
                # self.generar_incendios()
                # self.generar_robos()
                # self.generar_enfermedades()
                if int(self.tiempo) % T_SEMAFORO == 0:
                    # print('->', self.tiempo, 'cambioo')
                    if (int(self.tiempo) / T_SEMAFORO) % 2 == 0:
                        self.cambiar_semaforos('vertical')
                    else:
                        self.cambiar_semaforos('horizontal')
            # self.obtener_estadisticas()

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
    # print(city.max_autos)
    city.agregar_autos()
    city.interface.actualizar()
    # print([i.posicion for i in city.autos])
    city.interface.show()
    # print(len(city.autos))
    # print(city)
    # city.interface.tiempo_intervalo = 0.5
    city.posibles()
    # print(city)
    # city.interface.actualizar()
    app.exec_()
