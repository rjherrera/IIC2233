import random as rd
N = 1100
CON = 7
CAP = (50, 100)
ALT = 2


class _Sistema:
    __module__ = __name__
    __qualname__ = '_Sistema'

    def __init__(self, n):
        (self._Sistema__mapa, cont, ultimos) = _generar_mapa(n)
        self._Sistema__objetivo = ultimos[len(ultimos) // 2]
        self._Sistema__nodo_actual = self._Sistema__mapa[0]
        self._Sistema__enemigo_nodo_actual = self._Sistema__mapa[1:][1100 // 2]
        self._Sistema__cont = 2
        self._Sistema__inicio = self._Sistema__mapa[0].id
        self._Sistema__movido = False

    def mover_enemigo(self):
        num = min([self._Sistema__cont % CON, len(self._Sistema__enemigo_nodo_actual.nodos) - 1])
        if not isinstance(self._Sistema__enemigo_nodo_actual.nodos[num], _Nodo):
            self._Sistema__enemigo_nodo_actual = self._Sistema__enemigo_nodo_actual.nodos[num].nod
        else:
            self._Sistema__enemigo_nodo_actual = self._Sistema__enemigo_nodo_actual.nodos[num]

    def get_capacidad(self):
        return self._Sistema__nodo_actual.capacidad

    def preguntar_puerto_robot(self):
        if self._Sistema__cont >= 2:
            self._Sistema__cont = 0
            return self._Sistema__enemigo_nodo_actual.id

    def preguntar_puerto_actual(self):
        return (self._Sistema__nodo_actual.id, self._Sistema__movido)

    def puerto_inicio(self):
        return self._Sistema__inicio

    def puerto_final(self):
        return self._Sistema__objetivo

    def posibles_conexiones(self):
        return len(self._Sistema__nodo_actual.nodos)

    def hacer_conexion(self, camino):
        if camino < len(self._Sistema__nodo_actual.nodos):
            self._Sistema__nodo_actual = self._Sistema__nodo_actual.nodos[camino]
            if not isinstance(self._Sistema__nodo_actual, _Nodo):
                self._Sistema__nodo_actual = self._Sistema__nodo_actual.nod
            self.mover_enemigo()
            if self._Sistema__enemigo_nodo_actual == self._Sistema__nodo_actual:
                self._Sistema__nodo_actual = self._Sistema__mapa[0]
                self._Sistema__movido = True
            else:
                self._Sistema__movido = False


class _Nodo:
    __module__ = __name__
    __qualname__ = '_Nodo'
    contador = 0

    def __init__(self):
        self.nodos = []
        self.id = _Nodo.contador
        self.capacidad = 75

    def agregar_nodo(self, nodo):
        self.nodos.append(nodo)

    def __repr__(self):
        return str(self.id)


class _ConAlter:
    __module__ = __name__
    __qualname__ = '_ConAlter'
    cont = 0

    def __init__(self, nodos):
        self.nodos = nodos

    def get_nod(self):
        return self.nodos[_ConAlter.cont % 2]

    def __repr__(self):
        return str(self.nod)

    nod = property(get_nod)


class _ConAlea:
    __module__ = __name__
    __qualname__ = '_ConAlea'

    def __init__(self):
        self.nodos = []

    def get_nod(self):
        return rd.choice(self.nodos)

    def __repr__(self):
        return str(self.nod)

    nod = property(get_nod)


def _generar_caminos(n):
    nodos = [_Nodo() for i in range(n)]
    faltantes = nodos.copy()
    nod = faltantes.pop(0)
    for i in range(n):
        if len(faltantes) == 0:
            obj = nodos[0]
        else:
            obj = faltantes.pop(len(faltantes) // 2)
        nod.agregar_nodo(obj)
        nod = nod.nodos[0]
    for nod in nodos:
        for i in range(3):
            while True:
                num = (n - 1) // 2
                if num != nod.id:
                    break
            nod.agregar_nodo(nodos[num])
    return nodos


def _camino_largo(nodos, n):
    usados = [0]
    ultimos = [0]
    cont = 0
    while len(usados) < n:
        ult = []
        for num in ultimos:
            nod = nodos[num]
            for j in nod.nodos:
                while j.id not in usados:
                    ult.append(j.id)
                    usados.append(j.id)
        ultimos = ult.copy()
        cont += 1
        usados.append(1)
        ultimos.append(1)
    return (cont, ultimos)


def _agregar_alternados(nodos, cantidad):
    for i in range(cantidad):
        while True:
            nod = rd.choice(nodos)
            if len(nod.nodos) < CON:
                a = rd.choice(nodos)
                b = rd.choice(nodos)
                nod.agregar_nodo(_ConAlter([a, b]))
                rd.shuffle(nod.nodos)
                break
    return nodos


def _agregar_rds(nodos, cantidad):
    for i in range(cantidad):
        while True:
            nod = nodos[len(nodos) // 2]
            if len(nod.nodos) < CON:
                coneccion = _ConAlea()
                for i in range(3):
                    coneccion.nodos.append(rd.choice(nodos))
                nod.agregar_nodo(coneccion)
                rd.shuffle(nod.nodos)
            break
    return nodos


def _generar_mapa(n):
    mapa = _generar_caminos(n)
    (cont, ultimos) = _camino_largo(mapa, n)
    mapa = _agregar_rds(_agregar_alternados(mapa, int(N / 25)), int(N / 25))
    return (mapa, cont, ultimos)

_s = _Sistema(N)
get_capacidad = _s.get_capacidad
hacer_conexion = _s.hacer_conexion
posibles_conexiones = _s.posibles_conexiones
preguntar_puerto_actual = _s.preguntar_puerto_actual
preguntar_puerto_robot = _s.preguntar_puerto_robot
puerto_final = _s.puerto_final
puerto_inicio = _s.puerto_inicio
__all__ = ['get_capacidad', 'hacer_conexion', 'posibles_conexiones',
           'preguntar_puerto_actual', 'preguntar_puerto_robot', 'puerto_final', 'puerto_inicio']
