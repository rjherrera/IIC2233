# coding=utf-8
from data_structures2 import Arbol, pseudo_hash
from data_structures import List
import sistema as st
from sys import stdout
from random import choice


class Puerto:

    def __init__(self, id_puerto):
        self.id = id_puerto
        self.conexiones = List()
        self.capacidad = st.get_capacidad()

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
        self._tipo = 0

    @property
    def tipo(self):
        tipos = ['', ' ALT', ' RAND']
        index = 1 if self._tipo == 2 else 2 if self._tipo > 2 else 0
        return tipos[index]

    def __eq__(self, other):
        return self.origen == other.origen and self.destino == self.destino

    def __lt__(self, other):
        return self.id < other.id

    def __le__(self, other):
        return self.id <= other.id

    def __repr__(self):
        return 'Conexion(%s-->%s)' % (self.origen, self.destino)


class Ruta:

    def __init__(self, lista):
        self.camino = lista

    @property
    def flujo(self):
        return min(i.capacidad for i in self.camino)

    @property
    def flujos(self):
        return List(*(i.capacidad for i in self.camino))


class Grafo:

    def __init__(self):
        self.conexiones = List()
        self.puertos_id = Arbol()
        self.puertos = Arbol()
        # self.lista_puertos = List()
        self.conexiones_id = Arbol()
        self.ruta_bummer = None

    def mapear_red(self):
        '''
        Se itera sobre la red de modo de encontrar los puertos teniendo el
        id del puerto actual como el mayor y cambiandolo cada vez que se
        encuentre uno mayor, de modo de recorrerlos todos. Después se itera
        un numero indeterminado de veces sobre la red para obtener todas las
        conexiones. Se detiene una vez que 4 grupos seguidos de 100000
        iteraciones tengan el mismo numero de conexiones encontradas. En ambos
        casos (puertos y conexiones) se guardan ids en un arbol binario y
        objetos en otro arbol o lista, para hacer la comprobación de
        "objeto in contenedor" de forma óptima.
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
        while estable < 3:
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
                if len(self.conexiones) == n_anterior:
                    estable += 1  # comprueba que no cambien las cxs
                else:
                    estable = 0
                n_anterior = len(self.conexiones)
                print('.', end='')  # sublime syntax error, pero cumple pep
                stdout.flush()
            iteraciones += 1
        print('\n%d conexiones encontradas.' % len(self.conexiones))

    def alternantes_random(self):
        '''
        Por complejidad del problema, ya que es imposible encontrar la
        diferencia entre una "ruta" alternante de 2 destinos y una random
        de 2 destinos, se opta por asignar como alternantes a aquellas que
        presenten 2 destinos y como aleatorias a las que presenten más.
        iteraciones ~= n_conexiones * promedio_destinos_por_puerto
        '''
        for i in self.conexiones:
            for j in i.origen.conexiones:
                if i.id == j.id:
                    i._tipo += 1

    def ruta_a_bummer(self):
        '''
        Se busca la ruta mas corta por amplitud, de modo que se van
        agregando a una pila todos los puertos más proximos al actual
        y si alguno de ellos es el final, se retorna la ruta hasta ese
        momento, sino, se van agregando todos los caminos siguientes.
        El algoritmo es el BFS basado en lo encontrado en internet:
        http://stackoverflow.com/a/8922151
        :return: List de puertos con la Ruta más corta hasta bummer
        '''
        inicio = self.puertos.raiz
        final = Puerto(st.puerto_final())
        print('Obteniendo ruta a Bummer (%s).' % final)
        rutas = List()
        rutas.append(List(inicio))
        while len(rutas) > 0:
            ruta_actual = rutas.popleft()
            puerto = ruta_actual[-1]
            if puerto == final:
                self.ruta_bummer = Ruta(ruta_actual)
                print('Ruta a Bummer obtenida.')
                return ruta_actual
            for puerto_destino in puerto.puertos:
                nuevo_camino = List(*ruta_actual)
                nuevo_camino.append(puerto_destino)
                rutas.append(nuevo_camino)

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
        # DESCARTAR DOBLES SI RUTAS
        i = 0
        while i < len(dobles):
            j = 0
            while j < len(dobles):
                if dobles[i][-1] == dobles[j][0]:
                    nueva_conexion = dobles[i][:-1] + dobles[j]
                    dj = dobles[j]
                    dobles = dobles.remove(dobles[i])
                    dobles = dobles.remove(dj)
                    dobles.append(nueva_conexion)
                    j = 0
                j += 1
            i += 1
        # # DESCARTAR DOBLES SI RUTAS
        return dobles

    def rutas_triangulares(self):
        triangulos = List()
        for nodo in self.puertos:
            puerto = nodo.valor
            for destino in puerto.puertos:
                for destino_destino in destino.puertos:
                    for destino_destino_destino in destino_destino.puertos:
                        if destino_destino_destino == puerto:
                            # solo agregar si no es del tipo AAB, AAA, ABA
                            if (puerto != destino and
                                    destino != destino_destino and
                                    puerto != destino_destino):
                                triangulos.append(
                                    List(puerto, destino, destino_destino))
        # eliminar triangulos repetidos A-B-C -> BCA, CAB
        i = 0
        while i < len(triangulos):
            j = 0
            while j < len(triangulos):
                tr1 = List(triangulos[j][2],
                           triangulos[j][0],
                           triangulos[j][1])
                tr2 = List(triangulos[j][1],
                           triangulos[j][2],
                           triangulos[j][0])
                if triangulos[i] == tr1:
                    triangulos = triangulos.remove(tr1)
                    j = 0
                elif triangulos[i] == tr2:
                    j = 0
                    triangulos = triangulos.remove(tr2)
                j += 1
            i += 1
        return triangulos

    def rutas_cuadradas(self):
        cuadrados = List()
        for nodo in self.puertos:
            puerto = nodo.valor
            for destino in puerto.puertos:
                for des_des in destino.puertos:
                    for des_des_des in des_des.puertos:
                        for des_des_des_des in des_des_des.puertos:
                            c5 = puerto == destino == des_des == des_des_des
                            if des_des_des_des == puerto:
                                l = List(puerto, destino, des_des,
                                         des_des_des)
                                # solo agregar si no es de tipo AAAA, ABAB, etc
                                c1 = destino not in l.remove(destino)
                                c2 = puerto not in l.remove(puerto)
                                c3 = des_des not in l.remove(des_des)
                                c4 = des_des_des not in l.remove(des_des_des)
                                if c1 and c2 and c3 and c4 and not c5:
                                    cuad = List(puerto, destino, des_des,
                                                des_des_des)
                                    cuadrados.append(cuad)
        # eliminar cuadrados repetidos A-B-C-D -> BCDA, CDAB, DABC
        i = 0
        while i < len(cuadrados):
            j = 0
            while j < len(cuadrados):
                cd1 = List(cuadrados[j][3],
                           cuadrados[j][0],
                           cuadrados[j][1],
                           cuadrados[j][2])
                cd2 = List(cuadrados[j][2],
                           cuadrados[j][3],
                           cuadrados[j][0],
                           cuadrados[j][1])
                cd3 = List(cuadrados[j][1],
                           cuadrados[j][2],
                           cuadrados[j][3],
                           cuadrados[j][0])
                if cuadrados[i] == cd1:
                    cuadrados = cuadrados.remove(cd1)
                    j = 0
                elif cuadrados[i] == cd2:
                    j = 0
                    cuadrados = cuadrados.remove(cd2)
                elif cuadrados[i] == cd3:
                    j = 0
                    cuadrados = cuadrados.remove(cd3)
                j += 1
            i += 1
        return cuadrados

    def rutas_cortas(self, cantidad):
        '''
        Inspecciono la red para obtener "cantidad" rutas a bummer, de
        modo que se obtengan rutas cortas (porque es más probable que sean
        de capacidad máxima). Si alguna de estas rutas tiene como flujo la
        capacidad de el puerto final o inicial se retorna esta como la ruta
        por razones obvias.
        :return: List de las primeras "cantidad" rutas cortas a bummer
        '''
        rutas_totales = List()
        inicio = self.puertos.raiz
        final = Puerto(st.puerto_final())
        rutas = List()
        if self.ruta_bummer is not None:
            rutas.append(self.ruta_bummer.camino)
        else:
            rutas.append(List(inicio))
        iteraciones = 0
        print('Obteniendo rutas a Bummer...')
        while (len(rutas) > 0 and len(rutas_totales) < cantidad
                and iteraciones < 200000):
            ruta_actual = rutas.popleft()
            puerto = ruta_actual[-1]
            if puerto == final:
                nueva_ruta = Ruta(ruta_actual)
                rutas_totales.append(nueva_ruta)
                print('.', end='')
                stdout.flush()
                if (nueva_ruta.flujo == nueva_ruta.flujos[-1] or
                        nueva_ruta.flujo == nueva_ruta.flujos[0]):
                    print('\nRutas obtenidas.')
                    return rutas_totales
            for puerto_destino in puerto.puertos:
                nuevo_camino = List(*ruta_actual)
                nuevo_camino.append(puerto_destino)
                rutas.append(nuevo_camino)
            iteraciones += 1
        print('\nRutas obtenidas.')
        return rutas_totales

    def maximo_flujo(self, n_rutas_a_evaluar):
        '''
        Se obtiene el flujo máximo y la ruta correspondiente a ese flujo
        :return: List de flujo, ruta
        '''
        rutas = self.rutas_cortas(n_rutas_a_evaluar)
        if len(rutas) == 0:
            if self.ruta_bummer is None:
                self.ruta_a_bummer()
            return List(self.ruta_bummer.flujo, self.ruta_bummer)
        return max((List(i.flujo, i) for i in rutas),
                   key=lambda x: x[0])
