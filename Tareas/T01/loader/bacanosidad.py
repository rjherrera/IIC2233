# coding=utf-8
import numpy as np


def es_alumno(usuario):
    return hasattr(usuario, 'idolos')


# def bacanosidad(usuarios):
#     dicc = dict((i.nombre_completo, i) for i in usuarios.values())
#     for i in usuarios.values():
#         if es_alumno(i):
#             for j in i.idolos:
#                 if es_alumno(dicc[j]):
#                     dicc[j].bacanosidad_puntos += 1
#     for i in usuarios.values():
#         if es_alumno(i):
#             repartir = i.bacanosidad_puntos / len(i.idolos)
#             for j in i.idolos:
#                 if es_alumno(dicc[j]):
#                     dicc[j].bacanosidad_puntos += repartir
#     lista = [(i.nombre_completo, i.bacanosidad_puntos) for i in dicc.values() if es_alumno(i)]
#     print(max(lista, key=lambda x: x[1]))
#     for i in lista[:50]:
#         print(i[0], i[1])

def bacanosidad(usuarios):
    lista = [i for i in usuarios.values() if es_alumno(i)]
    lista = sorted(lista, key=lambda x: x.nombre_completo)
    m = np.zeros((len(lista), len(lista)))
    for i in range(len(lista)):
        for j in range(len(lista)):
            if lista[j].nombre_completo in lista[i].idolos:
                m[i][j] = 1 / len(lista[i].idolos)
    l = [i.nombre_completo for i in lista]
    for i in range(20):
        m = m ** 2  # multiplico hasta que converja
    mx = np.amax(m[0]) if np.amax(m[0]) != 0 else 1
    mx = m[0] / mx
    lista = [[i[0], i[1]] for i in zip(l, list(mx))]
    return list(lista)


def groups(lista, n):
    j = 0
    for i in range(0, len(lista), n):
        j += 1
        aux = [i + [j] for i in lista[i:i + n]]
        yield aux


def obtener_grupos(lista):
    l = sorted(lista, key=lambda x: -x[1])
    cantidad = len(l) // 10
    generador = groups(l, cantidad)
    bacanosidad_grupo = []
    for i in range(10):
        g = next(generador)
        bacanosidad_grupo.extend(g)
    return bacanosidad_grupo
