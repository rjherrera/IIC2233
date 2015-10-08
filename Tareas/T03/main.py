import os
from tablero import Tablero
from random import choice
from inputs import *


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
        tablero = self.tableros[jugador]
        print(tablero.letras_vehiculos)
        veh = pedir_restringido('Elija el vehículo con el que atacar (Ej: \'C\'): ',
                                ['B', 'b', 'C', 'E', 'K', 'L', 'P'])
        vehiculo = tablero.obtener_vehiculo_letra(veh)
        print(vehiculo.letras_ataques)
        if vehiculo.lista_letras_ataques:
            ata = pedir_restringido('Elija un ataque (Ej: \'T\'): ',
                                    vehiculo.lista_letras_ataques)
        else:
            print('No hay ataques disponibles en este vehículo.')
            return False
        ataque = vehiculo.obtener_ataque_letra(ata)
        if ataque.letra == 'I':
            pos = pedir_tupla('Elija una posición a la cual sanar (Ej: 0,1): ')
            ori = 'H'
        else:
            pos = pedir_tupla('Elija una posición a la cual atacar: ')
            ori = pedir_restringido('Elija la orientacion del ataque (H/V): ',
                                    ['H', 'V', 'v', 'h']).upper()
        if ataque.disponible and ataque.letra != 'I':
            fue, exitos, naves = vehiculo.ataque(self.tableros[receptor],
                                                 ataque, pos, ori)
            if repr(ataque) != 'MisilTomahawk' and exitos:
                print('El ataque fue exitoso en %s' % str(exitos)[1:-1])
                if naves:
                    print('Se destruyeron estas naves: %s' % str(naves)[1:-1])
                input('Presione cualquier tecla para continuar...')
            elif repr(ataque) == 'MisilTomahawk' and exitos:
                print('El ataque fue exitoso.')
            else:
                print('El ataque fue fallido.')
            return True
        elif ataque.disponible and ataque.letra == 'I':
            sanado = ataque.sanar(tablero, pos)
            sanado = sanado if sanado is not None else 'nadie'
            print('Se sanó a %r en 1 punto.' % sanado)
            return True
        else:
            print('Debe esperar %d turnos para usar este ataque.' %
                  ataque.recoil_actual)
            return False

    def mover(self, jugador, receptor):
        tablero = self.tableros[jugador]
        print(tablero.letras_vehiculos)
        veh = pedir_restringido('Elija el vehículo para mover (Ej: \'K\'): ',
                                ['B', 'b', 'C', 'E', 'K', 'L', 'P'])
        vehiculo = tablero.obtener_vehiculo_letra(veh)
        inicio_actual = vehiculo.posiciones_actuales[0]
        if repr(vehiculo) == 'Lancha':
            pos = pedir_tupla(
                'Elija una posición a la cual mover (Ej: 0,1): ')
        else:
            lado = pedir_restringido(
                'Elija el lado para moverse (der/izq/aba/arr): ',
                ['der', 'izq', 'aba', 'arr'])
            if lado == 'der':
                pos = (inicio_actual[0], inicio_actual[1] + 1)
            elif lado == 'izq':
                pos = (inicio_actual[0], inicio_actual[1] - 1)
            elif lado == 'aba':
                pos = (inicio_actual[0] + 1, inicio_actual[1])
            elif lado == 'arr':
                pos = (inicio_actual[0] - 1, inicio_actual[1])
        poss = vehiculo.generar_posiciones(pos)[vehiculo.orientacion]
        if 0 <= pos[0] < tablero.n and 0 <= pos[1] < tablero.n:
            tablero = tablero.maritimo
            if vehiculo.__class__ in tablero.__class__.aereos:
                tablero = tablero.aereo
            verificacion = tablero.verificar_posiciones(poss, tablero)
            if verificacion[0]:
                disponibles = tablero.verificar_disponibles_mov(poss, tablero,
                                                                vehiculo)
                if disponibles[0]:
                    for pos in poss:
                        tablero.asignar(tablero, pos, vehiculo)
                else:
                    pos = disponibles[1]
                    print('Está usado por otro vehículo.')
            else:
                pos = verificacion[1]
                print('Se encuentra fuera de rango.')
            vehiculo.posiciones_actuales = poss
        else:
            print('Se encuentra fuera de rango.')
            return True
        return True

    def radar(self, jugador, receptor):
        n = pedir_entero('Ingrese el número de turno a obtener: ')
        historia = self.tableros[jugador].historial_ataques
        if n in historia:
            print('Radar de turno n°%d:' % n)
            print(historia[n])
        else:
            print('No hubo ataques en ese turno.')
        input('Presione cualquier tecla para continuar...')
        return False

    def distribuir(self, jugador):
        tablero = self.tableros[jugador]
        while len(tablero.posicionados) < 7:
            print('Distribuyendo %s:' % jugador)
            print(tablero.letras_vehiculos)
            print(tablero)
            vehiculo = input('Elija un vehiculo para posicionar (Ej: \'B\'): ')
            try:
                vehiculo = tablero.obtener_vehiculo_unico(vehiculo)
            except KeyError as error:
                print(error.args[0])
                continue
            posicion = pedir_tupla(
                'Elija coordenadas para el vehículo (Ej: 0, 1): ')
            orientacion = pedir_restringido('Elija una orientacion (H/V): ',
                                            ['H', 'V', 'v', 'h']).upper()
            posiciones = tablero.obtener_posiciones(vehiculo,
                                                    posicion,
                                                    orientacion)
            tablero.posicionar(vehiculo, posiciones)

    def ejecutar(self):
        self.distribuir(self.jugador1)
        clean_screen()
        print('%s distribuido correctamente' % self.jugador1)
        self.distribuir(self.jugador2)
        print('%s distribuido correctamente' % self.jugador2)
        jugs = [self.jugador1, self.jugador2]
        primero = choice(jugs)
        # print(primero)
        segundo = [i for i in jugs if i != primero][0]
        turno = 1
        while self.sigue():
            clean_screen()
            if turno % 2 == 1:
                actual = primero
                siguiente = segundo
            else:
                actual = segundo
                siguiente = primero
            self.tableros[actual].turno_actual = turno
            self.tableros[siguiente].turno_actual = turno
            print('Turno n°%d. Juega %s.' % (turno, actual))
            print(self.tableros[actual])
            self.mostrar()
            eleccion = input('Ingrese una opcion: ')
            if eleccion == '4':
                return
            accion = self.opciones.get(eleccion)
            if accion:
                if accion(actual, siguiente):
                    turno += 1
                else:
                    print('Vuelva a intentarlo.')
            else:
                print('%s no es una de las opciones, pruebe de nuevo.'
                      % eleccion)
            self.tableros[actual].pasar_turno()
            if turno % 4 == 0:
                self.tableros[actual].revisar_hundidos()
                self.tableros[siguiente].revisar_hundidos()
                # se eliminan las "X" para poder moverse a esas posiciones.

    def sigue(self):
        # debe ser la condicion de q le mate todos los barcos sin incluir la lancha
        return True


if __name__ == '__main__':
    n = pedir_entero('Ingrese el tamaño del tablero: ')
    j1 = input('Ingrese el nombre del jugador 1: ')
    j2 = input('Ingrese el nombre del jugador 2: ')
    Menu(j1, j2, n).ejecutar()
