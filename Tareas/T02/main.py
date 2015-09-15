# import inspect
import sistema as st
from random import choice, shuffle

# all_functions = inspect.getmembers(sistema, inspect.isfunction)
# imported_stuff = dir(sistema)

print(st.preguntar_puerto_actual())
print(st.posibles_conexiones())
print(st.hacer_conexion(6))
print(st.preguntar_puerto_actual())
print(st.preguntar_puerto_actual())
print(st.puerto_inicio())
print(st.puerto_final())
print()
print(st.preguntar_puerto_robot())
# st.pregunta_nodo_actual()
print()
print(st.get_capacidad())


class Puerto:

    def __init__(self, id_puerto, puerto_anterior=None):
        self.id = id_puerto
        self.anterior = puerto_anterior
        self.siguientes = list(range(st.posibles_conexiones()))

    def __eq__(self, other):
        return self.id == other


class Camino:

    current_id = 1

    def __init__(self):
        self.id = self.__class__.current_id
        self.__class__.current_id += 1
        self.puerto_actual = Puerto(st.puerto_inicio())
        self.puertos = [self.puerto_actual]
        self.puerto_final = st.puerto_final()
        self.recorrido = str(self.id)

    def recorrer(self):
        actual = self.puerto_actual
        print(self.puerto_final, actual.id)
        if actual.id == self.puerto_final:
            return True
        shuffle(actual.siguientes)
        for siguiente in actual.siguientes:
            st.hacer_conexion(siguiente)
            id_siguiente = st.preguntar_puerto_actual()[0]
            if id_siguiente in self.puertos:
                puerto = self.obtener_puerto(id_siguiente)
            else:
                puerto = Puerto(id_siguiente, puerto_anterior=actual)
            self.puerto_actual = puerto
            self.recorrido += '-->%d' % id_siguiente
            return self.recorrer()
        return False

    def obtener_puerto(self, id_puerto):
        for puerto in self.puertos:
            if puerto.id == id_puerto:
                return puerto
        return None





        # self.recorrido += '-->'


camino = Camino()
camino.recorrer()



def obtener_camino():
    pass
