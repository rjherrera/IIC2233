# import inspect
import sistema as st
from random import choice, shuffle
from draft import List

# all_functions = inspect.getmembers(sistema, inspect.isfunction)
# imported_stuff = dir(sistema)

# print('actual:', st.preguntar_puerto_actual())
# print('posibl:', st.posibles_conexiones())
# st.hacer_conexion(6)
# print('- conexion con 6° -')
# print('actual:', st.preguntar_puerto_actual())
# print('inicio:', st.puerto_inicio())
# print('finals:', st.puerto_final())
# print('robots:', st.preguntar_puerto_robot())

# print('capaci:', st.get_capacidad())


class Puerto:

    puertos = List()

    def __init__(self, id_puerto):
        self.id = id_puerto
        self.__class__.puertos.append(self)

    def __repr__(self):
        return 'Puerto(%s)' % str(self.id)

    @classmethod
    def tiene_puerto(cls, id_puerto):
        for i in cls.puertos:
            if i.id == id_puerto:
                return True
        return False

    @classmethod
    def obtener_puerto(cls, id_puerto):
        for i in cls.puertos:
            if i.id == id_puerto:
                return i
        return None


class Arista:

    def __init__(self, origen=None, destino=None):
        self.origen = origen
        self.destino = destino

    def __eq__(self, other):
        return self.origen == other.origen and self.destino == self.destino

    def __repr__(self):
        return '%s-->%s' % (self.origen, self.destino)


class Grafo:

    def __init__(self):
        self.aristas = List()

    def agregar_arista(self, arista):
        self.aristas.append(arista)

    # def existe_arista(self, puerto_origen, puerto_destino):
    #     for i in self.aristas:
    #         if i.origen == puerto_origen and i.destino == puerto_destino:
    #             return True
    #     return False

    def encontrar_puertos(self):
        actual_max = 2
        n = 0
        print('Obteniendo puertos y conexiones, esto puede tardar...')
        # last_print = n
        # from sys import stdout
        # print('0.00%', end='|')
        # stdout.flush()
        while n <= actual_max:
            # if ((n % 200 == 0 or (n > st.N - 50 and (n - st.N) % 10 == 0))
            #         and n != last_print):
            #     print('{}%|'.format(round((n / st.N) * 100, 2)), end='')
            #     stdout.flush()
            #     last_print = n
            actual, atrapado = st.preguntar_puerto_actual()
            print(actual_max, n, actual)
            if Puerto.tiene_puerto(actual):
                puerto_origen = Puerto.obtener_puerto(actual)
            else:
                puerto_origen = Puerto(actual)
                n += 1
            siguiente = choice(range(st.posibles_conexiones()))
            st.hacer_conexion(siguiente)
            siguiente, atrapado = st.preguntar_puerto_actual()
            if Puerto.tiene_puerto(siguiente):
                puerto_destino = Puerto.obtener_puerto(siguiente)
            else:
                puerto_destino = Puerto(siguiente)
                n += 1
            arista = Arista(origen=puerto_origen, destino=puerto_destino)
            if arista not in self.aristas:
                self.agregar_arista(arista)
            actual_max = max(actual_max, siguiente)
        print('100.00%')
        print('Puertos y conexiones obtenidas.')

        def ruta_final(self):
            pass


def output_puertos_conexiones():
    grafo = Grafo()
    grafo.encontrar_puertos()
    print('Escribiendo en "red.txt"')
    with open('red.txt', 'w') as f:
        for puerto in Puerto.puertos:
            linea = 'PUERTO %s\n' % str(puerto.id)
            f.write(linea)
        for arista in grafo.aristas:
            linea = 'CONEXION %s %s\n' % (arista.origen.id, arista.destino.id)
            f.write(linea)
    print('Resultado escrito en "red.txt"')


if __name__ == '__main__':
    print(st.puerto_final())
    output_puertos_conexiones()
    print(st.puerto_final())
    print(st.puerto_inicio())
