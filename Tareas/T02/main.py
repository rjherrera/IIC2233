# coding=utf-8
import dumper


class Menu:

    def __init__(self, grafo):
        self.grafo = grafo
        self.opciones = {
            '1': self.red,
            '2': self.minima,
            '3': self.dobles,
            '4': self.ciclos,
            '5': self.maxima,
            '6': self.nocycl,
        }

    def mostrar(self):
        print('\nMenu:\n  ',
              '1: Exportar red\n  ',
              '2: Exportar ruta mínima a Bummer\n  ',
              '3: Exportar rutas de doble sentido\n  ',
              '4: Exportar ciclos triangulares y cuadrados\n  ',
              '5: Exportar ruta de máxima capacidad\n',
              '6: Exportar red sin ciclos\n',
              '7: Salir\n')

    def ejecutar(self):
        while True:
            self.mostrar()
            eleccion = input('Ingrese una opcion: ')
            if eleccion == '7':
                return
            accion = self.opciones.get(eleccion)
            if accion:
                accion()
            else:
                print('%s no es una de las opciones, pruebe de nuevo.'
                      % eleccion)

    def red(self):
        return dumper.output_puertos_conexiones(self.grafo, 'red.txt')

    def minima(self):
        return dumper.output_ruta_a_bummer(self.grafo, 'rutaABummer.txt')

    def dobles(self):
        return dumper.output_rutas_doble_sentido(
            self.grafo, 'rutasDobleSentido.txt')

    def ciclos(self):
        return dumper.output_ciclos(self.grafo, 'ciclos.txt')

    def maxima(self):
        return dumper.output_maximo_flujo(self.grafo, 'rutaMaxima.txt')

    def nocycl(self):
        return dumper.output_no_cycle(self.grafo, 'noCycle.txt')


if __name__ == '__main__':
    grafo = dumper.Grafo()
    grafo.mapear_red()
    Menu(grafo).ejecutar()
