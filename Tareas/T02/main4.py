from data_structures2 import Arbol, ArbolComplejo, pseudo_hash
from data_structures import List

from datetime import datetime

import sistema as st
from random import choice


class Puerto:

    puertos = List()

    def __init__(self, id_puerto, conexiones=0):
        self.id = id_puerto
        self.posibles_conexiones = (conexiones if conexiones
                                    else st.posibles_conexiones())
        self.conexiones = List()
        self.__class__.puertos.append(self)

    def __repr__(self):
        return 'Puerto(%s)' % str(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __lt__(self, other):
        return self.id < other.id

    def __le__(self, other):
        return self.id <= other.id


class Conexion:

    conexiones = List()

    def __init__(self, id, origen=None, destino=None):
        self.id = id
        self.origen = origen
        self.destino = destino
        # self.__class__.conexiones.append(self)

    def __eq__(self, other):
        return self.origen == other.origen and self.destino == self.destino

    def __repr__(self):
        return '%s-->%s' % (self.origen, self.destino)


class Grafo:

    # def tiene_puerto(self, id_puerto):
    #     for i in self.puertos:
    #         if i.id == id_puerto:
    #             return True
    #     return False

    def __init__(self):
        self.conexiones = ArbolComplejo()
        self.puertos = Arbol()

    # def agregar_conexion(self, conexion):
    #     self.conexiones.append(conexion)

    # def existe_conexion(self, puerto_origen, puerto_destino):
    #     for i in self.conexiones:
    #         if i.origen == puerto_origen and i.destino == puerto_destino:
    #             return True
    #     return False

    def encontrar_puertos(self):
        actual_max = 2
        n_puertos = 0
        n_iteraciones = 0
        print('Obteniendo puertos y conexiones, esto puede tardar...')
        while n_puertos <= actual_max:
            n_iteraciones += 1
            actual, atrapado = st.preguntar_puerto_actual()
            conexiones = st.posibles_conexiones()
            puerto_actual = Puerto(actual, conexiones)
            if puerto_actual not in self.puertos:
                n_puertos += 1
                self.puertos.add(puerto_actual)
            siguiente_index = choice(range(conexiones))
            st.hacer_conexion(siguiente_index)
            siguiente, atrapado = st.preguntar_puerto_actual()
            puerto_siguiente = Puerto(siguiente)
            if puerto_siguiente not in self.puertos:
                n_puertos += 1
                self.puertos.add(puerto_siguiente)
            actual_max = max(actual_max, siguiente)
        print('%d puertos obtenidos.' % n_puertos)
        # pctje_antes = n_conexiones_creadas / n_conexiones_totales * 100
        print(n_iteraciones, 'iteraciones:')##, n_conexiones_creadas, 'conexiones.')
        # while n_iteraciones <= 5000000:
        #     n_iteraciones += 1
        #     actual, atrapado = st.preguntar_puerto_actual()
        #     conexiones = st.posibles_conexiones()
        #     siguiente_index = choice(range(conexiones))
        #     st.hacer_conexion(siguiente_index)
        #     siguiente, atrapado = st.preguntar_puerto_actual()
        #     if n_iteraciones % 1000000 == 0:
        #         print(n_iteraciones, 'iteraciones:', n_conexiones_creadas, 'conexiones.')
        #     if pseudo_hash(actual, siguiente) not in self.conexiones:
        #         Conexion(id=siguiente_index,
        #                  origen=Puerto(actual),
        #                  destino=Puerto(siguiente))
        #         self.conexiones.add(actual, siguiente)
        #         n_conexiones_creadas += 1
        print(len(Conexion.conexiones))
        print(len(Puerto.puertos))
        # print('Iteraciones:', n_iteraciones)
        # print('Conexiones creadas:', n_conexiones_creadas)
        # print('Conexiones totales:', n_conexiones_totales)
        # print('Porcentaje:', n_conexiones_creadas/n_conexiones_totales * 100)
        # print('Porcentaje Antes:', pctje_antes)

    def obtener_doble_via(self):
        n = 0
        for conexion in Conexion.conexiones:
            if conexion.destino == conexion.origen:
                n += 1
        return n




def output_puertos_conexiones():
    grafo = Grafo()
    grafo.encontrar_puertos()
    return grafo
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
    i = datetime.utcnow()
    grafo = output_puertos_conexiones()
    grafo.obtener_doble_via()


    # with open('prueba.txt') as f:
    #     print(sum(int(i.strip().split()[3]) for i in f.readlines()))
    print(datetime.utcnow() - i)

    i = datetime.utcnow()
    print(datetime.utcnow() - i)
