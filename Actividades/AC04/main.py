# coding=utf-8
from collections import deque

# Completen los métodos
# Les estamos dando un empujoncito con la lectura del input
# Al usar la clausula: "with open('sonda.txt', 'r') as f", el archivo se cierra automáticamente al salir de la función.


def sonda():
    minerales = {}
    with open('sonda.txt', 'r') as f:
        for line in f:
            data = line.strip().split(',')
            key = tuple(int(i) for i in data[:4])
            minerales[key] = data[4]
    # asumo que me entregan un entero
    n_consultas = int(input('Número de consultas: '))
    i = 0
    while i < n_consultas:
        # asumo que me entregan coordenadas de la forma "0,0,0,0" o "0, 0, 0, 0"
        entrada = input('Ingrese coordenadas (separadas por coma): ')
        coords = tuple(int(i) for i in entrada.replace(' ', '').split(','))
        if coords in minerales:
            print(minerales[coords])
        else:
            print('No hay nada')
        i += 1


def traidores():
    bufalos = set()
    with open('bufalos.txt', 'r') as f:
        for line in f:
            bufalos.add(line.strip())
    rivales = set()
    with open('rivales.txt', 'r') as f:
        for line in f:
            rivales.add(line.strip())
    traids = bufalos.intersection(rivales)
    for traidor in traids:
        print(traidor)


def pizzas():
    cola = deque()
    pila = deque()
    cont_cola = 1
    cont_pila = 1
    with open('pizzas.txt', 'r') as f:
        for line in f.read().splitlines():
            if line == 'APILAR':
                pila.append(cont_pila)
                print('Pizza %d apilada' % cont_pila, end='. ')
                cont_pila += 1
            elif line == 'ENCOLAR':
                pizza = pila.pop()
                cola.append(pizza)
                cont_cola += 1
                print('Pizza %d encolada' % pizza, end='. ')
            elif line == 'SACAR':
                pizza_sacada = cola.popleft()
                print('Pizza %d sacada' % pizza_sacada, end='. ')
            str_pila = 'Pizza apilada' if len(pila) == 1 else 'Pizzas apiladas'
            str_cola = 'Pizza en cola' if len(cola) == 1 else 'Pizzas en cola'
            print('%d %s - %d %s' % (len(pila), str_pila, len(cola), str_cola))



if __name__ == '__main__':
    exit_loop = False

    functions = {"1": sonda, "2": traidores, "3": pizzas}

    while not exit_loop:
        print(""" Elegir problema:
            1. Sonda
            2. Traidores
            3. Pizzas
            Cualquier otra cosa para salir
            Respuesta: """)

        user_entry = input()

        if user_entry in functions:
            functions[user_entry]()
        else:
            exit_loop = True
