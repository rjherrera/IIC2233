#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
from datetime import datetime
import pickle


class Persona:

    def __init__(self, _id, nombre_completo, amigos=[], persona_favorita=''):
        self.id = _id
        self.nombre_completo = nombre_completo
        self.amigos = amigos
        self.persona_favorita = persona_favorita
        self.n_guardados = 0
        self.ultimo_guardado = None

    def __getstate__(self):
        dicc = self.__dict__.copy()
        dicc['n_guardados'] += 1
        dicc['ultimo_guardado'] = datetime.now()
        return dicc

    def __setstate__(self, estado):
        self.__dict__ = estado

    # @property
    # def ultimo_guardado(self):
    #     return self._ultimo_guardado

    # @ultimo_guardado.setter
    # def ultimo_guardado(self, value):
    #     self.n_guardados += 1
    #     self._ultimo_guardado = value


def existe_persona(_id):
    return _id + '.iic2233' in os.listdir('db')


def get_persona(_id):
    if existe_persona(_id):
        with open('db/' + _id + '.iic2233', 'rb') as file:
            return pickle.load(file)
    return None


def write_persona(persona):
    with open('db/' + persona.id + '.iic2233', 'wb') as file:
        pickle.dump(persona, file)


def crear_persona(_id, nombre_completo):
    if not existe_persona(_id):
        persona = Persona(_id, nombre_completo)
        write_persona(persona)


def agregar_amigo(id_1, id_2):
    if existe_persona(id_1) and existe_persona(id_2):
        persona = get_persona(id_1)
        if id_2 not in persona.amigos:
            persona.amigos.append(id_2)
        write_persona(persona)
        persona_2 = get_persona(id_2)
        if id_1 not in persona_2.amigos:
            persona_2.amigos.append(id_1)
        write_persona(persona_2)


def set_persona_favorita(_id, id_favorito):
    if existe_persona(_id) and existe_persona(id_favorito):
        persona = get_persona(_id)
        persona.persona_favorita = id_favorito
        write_persona(persona)


def get_persona_mas_favorita():
    lista_personas = [get_persona(i.split('.')[0]) for i in os.listdir('db')]
    # asumo que solo hay esos archivos en la carpeta db, funciona en linux
    # parece que en mac se crean archivos raros pero en mi pc funciona
    lista_favs = [[i.nombre_completo, 0, i.id] for i in lista_personas]
    for persona in lista_personas:
        fav = persona.persona_favorita
        for lista in lista_favs:
            if fav == lista[2]:
                lista[1] += 1
    return tuple(max(lista_favs, key=lambda x: x[1]))[:2]

# ----------------------------------------------------- #
# Codigo para probar su tarea - No necesitan entenderlo #


def print_data(persona):
    if persona is None:
        print("[AVISO]: get_persona no está implementado")
        return

    for key, val in persona.__dict__.items():
        print("{} : {}".format(key, val))
    print("-" * 80)


# Metodo que sirve para crear el directorio db si no existia #

def make_dir():
    if not os.path.exists("./db"):
        os.makedirs("./db")


if __name__ == '__main__':
    make_dir()
    crear_persona("jecastro1", "Jaime Castro")
    crear_persona("bcsaldias", "Belen Saldias")
    crear_persona("kpb", "Karim Pichara")
    set_persona_favorita("jecastro1", "bcsaldias")
    set_persona_favorita("bcsaldias", "kpb")
    set_persona_favorita("kpb", "kpb")
    agregar_amigo("kpb", "jecastro1")
    agregar_amigo("kpb", "bcsaldias")
    agregar_amigo("jecastro1", "bcsaldias")

    jecastro1 = get_persona("jecastro1")
    bcsaldias = get_persona("bcsaldias")
    kpb = get_persona("kpb")

    print_data(jecastro1)
    print_data(bcsaldias)
    print_data(kpb)

    print(get_persona_mas_favorita())
