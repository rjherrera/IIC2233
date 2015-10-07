import os
from tablero2 import Tablero
from random import choice

# def posicionar(tablero):
#     while


# while True:
#     try:
#         n = input('Ingrese el tamaño del tablero (entero): ')
#         tab = Tablero(int(n))
#     except ValueError:
#         print('%s no es un entero.' % n)

def clean_screen():
    for _ in range(5):
        os.system('cls' if os.name == 'nt' else 'clear')


class Menu:

    def __init__(self, jugador1, jugador2, n):
        self.tableros = {jugador1: Tablero(n), jugador2: Tablero(n)}
        self.jugador1 = jugador1
        self.jugador2 = jugador2
        self.opciones = {
            '1': self.atacar,
            '2': self.mover,
            '3': self.radar
        }

    def mostrar(self):
        print('\nMenu:\n  ',
              '1: Atacar\n  ',
              '2: Mover\n  ',
              '3: Ver el radar\n  ',
              '4: Salir')

    def atacar(self, jugador, receptor):
        self.tableros[jugador].atacar(self.tableros[receptor])

    def ejecutar(self):
        self.tableros[self.jugador1].distribuir()
        clean_screen()
        print('%s distribuido correctamente' % self.jugador1)
        self.tableros[self.jugador2].distribuir()
        print('%s distribuido correctamente' % self.jugador2)
        jugs = [self.jugador1, self.jugador2]
        primero = choice(jugs)
        segundo = [i for i in jugs if i != primero][0]
        turno = 0
        while True:
            if turno % 2 == 0:
                actual = primero
                siguiente = segundo
            else:
                actual = segundo
                siguiente = primero
            self.mostrar()
            eleccion = input('Ingrese una opcion: ')
            if eleccion == '4':
                return
            accion = self.opciones.get(eleccion)
            if accion:
                accion(actual, siguiente)
            else:
                print('%s no es una de las opciones, pruebe de nuevo.'
                      % eleccion)
            turno += 1


if __name__ == '__main__':
    while True:
        n = input('Ingrese el tamaño entero del tablero: ')
        try:
            n = int(n)
            break
        except ValueError:
            print('%r no es un entero válido' % n)
    j1 = input('Ingrese el nombre del jugador 1: ')
    j2 = input('Ingrese el nombre del jugador 2: ')
    Menu(j1, j2, n).ejecutar()
