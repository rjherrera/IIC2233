from data_structures import List
from datetime import datetime

import sistema as st
from random import choice, shuffle
GLOVAL = []


class Puerto:

    def __init__(self, id_puerto):
        self.id = id_puerto
        self.posibles_conexiones = st.posibles_conexiones()
        # self.__class__.puertos.append(self)

    def __repr__(self):
        return 'Puerto(%s)' % str(self.id)

    def __eq__(self, other):
        return self.id == other.id


class Conexion:

    current_id = 1

    def __init__(self, origen=None, destino=None):
        self.id = self.__class__.current_id
        self.__class__.current_id += 1
        self.origen = origen
        self.destino = destino

    def __eq__(self, other):
        return self.origen == other.origen and self.destino == self.destino

    def __repr__(self):
        return '%s-->%s' % (self.origen, self.destino)


class Grafo:

    def tiene_puerto(self, id_puerto):
        for i in self.puertos:
            if i.id == id_puerto:
                return True
        return False

    def __init__(self):
        self.conexiones = []
        self.puertos = []
        i = st.puerto_inicio()
        f = st.puerto_final()
        Puerto(i)
        Puerto(f)

    def agregar_conexion(self, conexion):
        self.conexiones.append(conexion)

    # def existe_conexion(self, puerto_origen, puerto_destino):
    #     for i in self.conexiones:
    #         if i.origen == puerto_origen and i.destino == puerto_destino:
    #             return True
    #     return False

    def encontrar_puertos(self):
        actual_max = 2
        n = 0
        contador = 0
        n_conexiones = 0
        print('Obteniendo puertos y conexiones, esto puede tardar...')
        # last_print = n
        # from sys import stdout
        # print('0.00%', end='|')
        # stdout.flush()
        while n <= actual_max:
            contador += 1
            # if ((n % 200 == 0 or (n > st.N - 50 and (n - st.N) % 10 == 0))
            #         and n != last_print):
            #     print('{}%|'.format(round((n / st.N) * 100, 2)), end='')
            #     stdout.flush()
            #     last_print = n
            actual, atrapado = st.preguntar_puerto_actual()
            conexiones = st.posibles_conexiones()
            print(actual_max, n, actual, conexiones)
            puerto_origen = Puerto(actual)
            if not self.tiene_puerto(actual):
                n += 1
                self.puertos.append(puerto_origen)
            siguiente = choice(range(conexiones))
            st.hacer_conexion(siguiente)
            siguiente, atrapado = st.preguntar_puerto_actual()
            puerto_destino = Puerto(siguiente)
            if not self.tiene_puerto(siguiente):
                n += 1
                self.puertos.append(puerto_destino)
            conexion = Conexion(origen=puerto_origen, destino=puerto_destino)
            if conexion not in self.conexiones:
                self.conexiones.append(conexion)
                n_conexiones += 1
            actual_max = max(actual_max, siguiente)
        # print('100.00%')
        print('iteraciones:', contador)
        print(n_conexiones)
        print('Puertos y conexiones obtenidas.')

        def ruta_final(self):
            pass


def output_puertos_conexiones():
    grafo = Grafo()
    grafo.encontrar_puertos()
    # print('Escribiendo en "red.txt"')
    # with open('red.txt', 'w') as f:
    #     for puerto in Puerto.puertos:
    #         linea = 'PUERTO %s\n' % str(puerto.id)
    #         f.write(linea)
    #     for conexion in grafo.conexiones:
    #         linea = 'CONEXION %s %s\n' % (conexion.origen.id, conexion.destino.id)
    #         f.write(linea)
    # print('Resultado escrito en "red.txt"')


















if __name__ == '__main__':
    output_puertos_conexiones()
    a = []
    x = 0
    for i in GLOVAL:
        if i not in a:
            x += i.posibles_conexiones
            a.append(i)
    print(x)
    print(len(GLOVAL))
    with open('prueba.txt') as f:
        print(sum(int(i.strip().split()[3]) for i in f.readlines()))
    i = datetime.utcnow()
    a = List()
    for _ in range(100000):
        a.append('a')
    print(datetime.utcnow() - i)

    i = datetime.utcnow()
    b = []
    for _ in range(100000):
        b.append('b')
    print(datetime.utcnow() - i)