from tablero import Tablero


# def posicionar(tablero):
#     while


# while True:
#     try:
#         n = input('Ingrese el tamaño del tablero (entero): ')
#         tab = Tablero(int(n))
#     except ValueError:
#         print('%s no es un entero.' % n)


class Menu:

    def __init__(self, jugador1, jugador2, n):
        self.tableros = {'j1': Tablero(n), 'j2': Tablero(n)}
        # self.opciones = {
        #     '1': self.red,
        #     '2': self.minima,
        #     '3': self.dobles,
        #     '4': self.ciclos,
        #     '5': self.maxima,
        #     '6': self.nocycl,
        # }

    def mostrar(self):
        print('\nMenu:\n  ',
              '1: Exportar red\n  ',
              '2: Exportar ruta mínima a Bummer\n  ',
              '3: Exportar rutas de doble sentido\n  ',
              '4: Exportar ciclos triangulares y cuadrados\n  ',
              '5: Exportar ruta de máxima capacidad\n  ',
              '6: Exportar red sin ciclos\n  ',
              '7: Salir\n')

    def ejecutar(self):
        self.tableros['j1'].distribuir()
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
        self.tableros['j2'].distribuir()
        while True:
            self.mostrar()
            eleccion = input('Ingrese una opcion: ')
            # if eleccion == '7':
            #     return
            # accion = self.opciones.get(eleccion)
            # if accion:
            #     accion()
            # else:
            #     print('%s no es una de las opciones, pruebe de nuevo.'
            #           % eleccion)


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
