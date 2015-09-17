from data_structures2 import Arbol, pseudo_hash
from data_structures import List

from datetime import datetime

import sistema as st
from random import choice


class Puerto:

    # puertos = List()

    def __init__(self, id_puerto, conexiones=0):
        self.id = id_puerto
        self.posibles_conexiones = (conexiones if conexiones
                                    else st.posibles_conexiones())
        self.conexiones = List()
        # self.__class__.puertos.append(self)

    @property
    def puertos(self):
        return List(*(conexion.destino for conexion in self.conexiones))

    def __repr__(self):
        return 'Puerto(%s)' % str(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __lt__(self, other):
        return self.id < other.id

    def __le__(self, other):
        return self.id <= other.id


class Conexion:

    # conexiones = List()

    def __init__(self, id, origen=None, destino=None):
        self.id = id
        self.origen = origen
        self.destino = destino
        # self.__class__.conexiones.append(self)

    def __eq__(self, other):
        return self.origen == other.origen and self.destino == self.destino

    def __lt__(self, other):
        return self.id < other.id

    def __le__(self, other):
        return self.id <= other.id

    def __repr__(self):
        return 'Conexion(%s-->%s)' % (self.origen, self.destino)


class Grafo:

    def __init__(self):
        self.conexiones = List()
        self.puertos_id = Arbol()
        self.puertos = Arbol()
        self.lista_puertos = List()
        self.conexiones_id = Arbol()

    def encontrar_puertos(self):
        '''
        Se itera sobre la red de modo de encontrar los puertos teniendo el
        id del puerto actual como el mayor y cambiandolo cada vez que se
        encuentre uno mayor, de modo de recorrerlos todos. Después se itera
        un numero razonable de veces sobre la red para obtener todas las
        conexiones. En ambos casos se guardan ids en un arbol binario y
        objetos en otro arbol o lista, para hacer la comprobación de
        "objeto in contenedor" e forma óptima.
        :return: None
        '''
        iteraciones = 0
        n_puertos = 0
        actual_max = 2
        n_conexiones = 0
        print('Obteniendo puertos...')
        while n_puertos <= actual_max:
            id_actual, atrapado = st.preguntar_puerto_actual()
            if id_actual not in self.puertos_id:
                puerto_actual = Puerto(id_actual)
                self.puertos.add(puerto_actual)
                self.puertos_id.add(id_actual)
                self.lista_puertos.append(puerto_actual)
                n_puertos += 1
            conexiones = st.posibles_conexiones()
            siguiente_index = choice(range(conexiones))
            st.hacer_conexion(siguiente_index)
            id_siguiente, atrapado = st.preguntar_puerto_actual()
            if id_siguiente not in self.puertos_id:
                puerto_siguiente = Puerto(id_siguiente)
                self.puertos.add(puerto_siguiente)
                self.puertos_id.add(id_siguiente)
                self.lista_puertos.append(puerto_siguiente)
                n_conexiones += conexiones
                n_puertos += 1
            iteraciones += 1
            actual_max = max(actual_max, id_siguiente)
        print('%d puertos encontrados' % len(self.puertos),
              'en %d iteraciones.' % iteraciones)
        print('Obteniendo conexiones...')
        while iteraciones < 2000000:
            id_actual, atrapado = st.preguntar_puerto_actual()
            conexiones = st.posibles_conexiones()
            siguiente_index = choice(range(conexiones))
            st.hacer_conexion(siguiente_index)
            id_siguiente, atrapado = st.preguntar_puerto_actual()
            if not atrapado:
                phash = pseudo_hash(id_actual, id_siguiente)
                if phash not in self.conexiones_id:
                    puerto_actual = self.puertos.find(Puerto(id_actual))
                    puerto_siguiente = self.puertos.find(Puerto(id_siguiente))
                    c = Conexion(siguiente_index,
                                 puerto_actual,
                                 puerto_siguiente)
                    self.conexiones.append(c)
                    self.conexiones_id.add(phash)
                    puerto = self.puertos.find(puerto_actual)
                    if puerto is not None:
                        puerto.conexiones.append(c)
            if iteraciones % 200000 == 0:
                from sys import stdout
                print('.', end='')  # sublime dice syntax error, pero está bien
                stdout.flush()
                # print(iteraciones, 'iteraciones:',
                #       len(self.conexiones), 'conexiones.')
            iteraciones += 1
        # print(self.puertos.nodo_raiz.valor.conexiones)
        # print(self.puertos.nodo_raiz.valor.puertos)
        print('\n%d conexiones encontradas.' % len(self.conexiones))

    def obtener_doble_via(self):
        '''
        Se itera sobre la red de modo de obtener todos los puertos que
        funcionan bidireccionalmente.
        :return: List con conexiones que funcionan para ambos sentidos.
        '''
        dobles = List()
        for nodo in self.puertos:
            puerto = nodo.valor
            for conexion in puerto.conexiones:
                destino = self.puertos.find(conexion.destino)
                for conexion2 in destino.conexiones:
                    if conexion2.destino == puerto:
                        if Conexion(0, destino, puerto) not in dobles:
                            dobles.append(conexion)
        return dobles

    def output_puertos_conexiones(self, ruta):  # ejecutar post encontrar ruta
        print('Escribiendo en "%s"' % ruta)
        with open(ruta, 'w') as f:
            for puerto in grafo.lista_puertos:
                linea = 'PUERTO %s\n' % str(puerto.id)
                f.write(linea)
            for conexion in grafo.conexiones:
                linea = ('CONEXION %s %s\n' %
                         (conexion.origen.id, conexion.destino.id))
                f.write(linea)
        print('Resultado escrito en "%s"' % ruta)

    def ruta_a_bummer(self, ruta):
        inicio = grafo.puertos.nodo_raiz.valor
        final = Puerto(st.puerto_final())
        queue = List()
        queue.append(List(inicio))
        while len(queue) > 0:
            path = queue.popleft()
            node = path[-1]
            if node == final:
                print('Escribiendo en "%s"' % ruta)
                with open(ruta, 'w') as f:
                    for i in range(len(path)):
                        if i < len(path) - 1:
                            origen = path[i].id
                            destino = path[i + 1].id
                            f.write('CONEXION %d %d\n' % (origen, destino))
                print('Resultado escrito en "%s"' % ruta)
                return path
            for adjacent in node.puertos:
                new_path = List(*path)
                new_path.append(adjacent)
                queue.append(new_path)


if __name__ == '__main__':
    i = datetime.utcnow()
    grafo = Grafo()
    grafo.encontrar_puertos()
    print(datetime.utcnow() - i)
    i = datetime.utcnow()
    grafo.output_puertos_conexiones(ruta='red.txt')
    print(datetime.utcnow() - i)
    i = datetime.utcnow()
    dobles = grafo.obtener_doble_via()
    print(dobles, len(dobles))
    print(datetime.utcnow() - i)

    i = datetime.utcnow()
    print('Final', Puerto(st.puerto_final()))
    print('Ruta a bummer:', grafo.ruta_a_bummer('rutaABummer.txt'))
    print(datetime.utcnow() - i)

    i = datetime.utcnow()
    # with open('prueba.txt') as f:
    #     print(sum(int(i.strip().split()[3]) for i in f.readlines()))
    print(datetime.utcnow() - i)

    i = datetime.utcnow()
    print(datetime.utcnow() - i)
