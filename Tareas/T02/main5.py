from data_structures2 import Arbol, pseudo_hash
from data_structures import List

from datetime import datetime

import sistema as st
from random import choice


class Puerto:

    def __init__(self, id_puerto, conexiones=0):
        self.id = id_puerto
        self.posibles_conexiones = (conexiones if conexiones
                                    else st.posibles_conexiones())
        self.conexiones = List()

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

    def __init__(self, id, origen=None, destino=None):
        self.id = id
        self.origen = origen
        self.destino = destino

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
        # self.lista_puertos = List()
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
                # self.lista_puertos.append(puerto_actual)
                n_puertos += 1
            conexiones = st.posibles_conexiones()
            siguiente_index = choice(range(conexiones))
            st.hacer_conexion(siguiente_index)
            id_siguiente, atrapado = st.preguntar_puerto_actual()
            if id_siguiente not in self.puertos_id:
                puerto_siguiente = Puerto(id_siguiente)
                self.puertos.add(puerto_siguiente)
                self.puertos_id.add(id_siguiente)
                # self.lista_puertos.append(puerto_siguiente)
                n_conexiones += conexiones
                n_puertos += 1
            iteraciones += 1
            actual_max = max(actual_max, id_siguiente)
        n_puertos = len(self.puertos)
        print('%d puertos encontrados' % n_puertos,
              'en %d iteraciones.' % iteraciones)
        print('Obteniendo conexiones...')
        estable = 0
        n_anterior = 0
        while estable < 2:
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
            if iteraciones % 500000 == 0:
                if len(self.conexiones) == n_anterior:
                    estable += 1  # comprueba que no cambien las cxs
                n_anterior = len(self.conexiones)
                from sys import stdout
                print('.', end='')  # sublime syntax error, pero está bien
                stdout.flush()
            iteraciones += 1
        print('\n%d conexiones encontradas.' % len(self.conexiones))

    def rutas_doble_sentido(self):
        '''
        Se itera sobre la red de modo de obtener todos los puertos que
        funcionan bidireccionalmente. Descarta las de destino == origen
        :return: List con conexiones que funcionan para ambos sentidos.
        '''
        dobles = List()
        for nodo in self.puertos:
            puerto = nodo.valor
            for destino in puerto.puertos:
                for destino_destino in destino.puertos:
                    if destino_destino == puerto:
                        if (Conexion(0, destino, puerto) not in dobles
                                and destino != puerto):
                            dobles.append(Conexion(0, puerto, destino))
        dobles = List(*(List(i.origen, i.destino) for i in dobles))
        # # DESCARTAR DOBLES SI TRIPLES O ENESIMAS
        return dobles

    def output_rutas_doble_sentido(self, ruta):
        dobles = self.rutas_doble_sentido()
        print('Escribiendo rutas de doble sentido en "%s"' % ruta)
        with open(ruta, 'w') as f:
            for conexion in dobles:
                if len(conexion) == 2:
                    f.write('PAR %d %d\n' % (conexion[0].id, conexion[1].id))
                elif len(conexion) > 2:
                    linea = 'RUTA %d' % conexion[0].id
                    for i in conexion[1:]:
                        linea += ' ' + str(i.id)
                    f.write(linea + '\n')
        print('Resultado escrito en "%s"' % ruta)

    def output_puertos_conexiones(self, ruta):
        print('Escribiendo puertos y conexiones en "%s"' % ruta)
        with open(ruta, 'w') as f:
            for nodo in grafo.puertos:  # puerto in grafo.lista_puertos
                linea = 'PUERTO %s\n' % str(nodo.valor.id)  # puerto.id
                f.write(linea)
            for conexion in grafo.conexiones:
                linea = ('CONEXION %s %s\n' %
                         (conexion.origen.id, conexion.destino.id))
                f.write(linea)
        print('Resultado escrito en "%s"' % ruta)

    def ruta_a_bummer(self):
        '''
        Algoritmo BFS basado en lo encontrado en internet
        '''
        inicio = grafo.puertos.raiz
        final = Puerto(st.puerto_final())
        rutas = List()
        rutas.append(List(inicio))
        while len(rutas) > 0:
            ruta_actual = rutas.popleft()
            puerto = ruta_actual[-1]
            if puerto == final:
                return ruta_actual
            for puerto_destino in puerto.puertos:
                nuevo_camino = List(*ruta_actual)
                nuevo_camino.append(puerto_destino)
                rutas.append(nuevo_camino)

    def output_ruta_a_bummer(self, ruta):
        ruta_minima = self.ruta_a_bummer()
        print('Escribiendo en "%s"' % ruta)
        with open(ruta, 'w') as f:
            for i in range(len(ruta_minima)):
                if i < len(ruta_minima) - 1:
                    origen = ruta_minima[i].id
                    destino = ruta_minima[i + 1].id
                    f.write('CONEXION %d %d\n' % (origen, destino))
        print('Resultado escrito en "%s"' % ruta)


if __name__ == '__main__':
    i = datetime.utcnow()
    grafo = Grafo()
    grafo.encontrar_puertos()
    print('\nMapearlared:', datetime.utcnow() - i)

    i = datetime.utcnow()
    grafo.output_puertos_conexiones(ruta='red.txt')
    print('Outputmapeo:', datetime.utcnow() - i)

    i = datetime.utcnow()
    print('\nPuertofinal:', Puerto(st.puerto_final()))
    grafo.output_ruta_a_bummer(ruta='rutaABummer.txt')
    print('rutaABummer:', datetime.utcnow() - i)

    i = datetime.utcnow()
    print()
    grafo.output_rutas_doble_sentido(ruta='rutasDobleSentido.txt')
    print('Dossentidos:', datetime.utcnow() - i)

    # i = datetime.utcnow()
    # with open('prueba.txt') as f:
    #     print(sum(int(i.strip().split()[3]) for i in f.readlines()))
    # print(datetime.utcnow() - i)

    # i = datetime.utcnow()
    # print(datetime.utcnow() - i)
