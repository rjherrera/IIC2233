from vehiculos import *


class Tablero:

    maritimos = [BarcoPequeno, BuqueDeGuerra, Lancha, Puerto]
    aereos = [AvionExplorador, AvionKamikazeIXXI, AvionCaza]

    def __init__(self, n):
        self.n = n
        self.maritimo = [[' ' for i in range(n)] for i in range(n)]
        self.aereo = [[' ' for i in range(n)] for i in range(n)]
        self.maritimos = {i.__name__: i() for i in self.__class__.maritimos}
        self.aereos = {i.__name__: i() for i in self.__class__.aereos}

    def __contains__(self, element):
        for i in range(self.n):
            if element in self.aereo[i] or element in self.maritimo[i]:
                return True
        return False

    def __str__(self):
        string = 'Marítimo:'.ljust(self.n * 4) + '  :··: Aéreo:\n'
        for i in range(self.n):
            string += '| ' + ' | '.join(self.maritimo[i]) + ' | :··: '
            string += '| ' + ' | '.join(self.aereo[i]) + ' |\n'
        return string

    def asignar(self, lista, posicion, vehiculo):
        if lista[posicion[0]][posicion[1]] != ' ':
            raise ValueError('Espacio usado por otro vehículo.')
        lista[posicion[0]][posicion[1]] = vehiculo.letra

    def obtener_vehiculo(self, nombre_vehiculo):
        if nombre_vehiculo not in self.maritimos:
            if nombre_vehiculo not in self.aereos:
                raise KeyError('Vehiculo %s no encontrado.' % nombre_vehiculo)
            return self.aereos[nombre_vehiculo]
        return self.maritimos[nombre_vehiculo]
        # try:
        #     vehic = self.maritimos[nombre_vehiculo]
        #     return vehic
        # except KeyError:
        #     try:
        #         vehic = self.aereos[nombre_vehiculo]
        #         return vehic
        #     except KeyError:
        #         print('Vehiculo %s no encontrado.' % nombre_vehiculo)

    def obtener_posiciones(self, vehiculo, posicion, orientacion):
        try:
            posiciones = vehiculo.generar_posiciones(posicion)[orientacion]
            return posiciones
        except KeyError:
            raise KeyError('%r no es una orientacion válida.' % orientacion)
        except TypeError:
            raise TypeError('%r no es un par de coordenadas válido.' % posicion)

    def verificar_posiciones(self, posiciones):
        for pos in posiciones:
            try:
                self.maritimo[pos[0]][pos[1]]
            except IndexError:
                return False, pos
        return True, None

    def posicionar(self, nombre_vehiculo, posicion, orientacion):
        try:
            vehiculo = self.obtener_vehiculo(nombre_vehiculo)
            posiciones = self.obtener_posiciones(vehiculo, posicion, orientacion)
            tablero = self.maritimo
            if vehiculo.__class__ in self.__class__.aereos:
                tablero = self.aereo
            if vehiculo.letra not in self:
                verificacion = self.verificar_posiciones(posiciones)
                if verificacion[0]:
                    for pos in posiciones:
                        self.asignar(tablero, pos, vehiculo)
                else:
                    pos = verificacion[1]
                    raise IndexError
                vehiculo.posiciones_actuales = posiciones
            else:
                print('%s ya posicionado.' % nombre_vehiculo)
        except (KeyError, ValueError, TypeError) as err:
            print(err.args[0], type(err))
        except IndexError as err:
            print('%r se encuentra fuera de rango.' % (pos,))

    def distribuir(self):
        print(self.aereos, self.maritimos)
        vehiculo = input('Elija un vehiculo para posicionar (Ej: \'B\'): ')
        posicion = input('Elija coordenadas para el vehículo (Ej: 0, 1): ')
        orientacion = input('Elija una orientacion (H/V): ').upper()



if __name__ == '__main__':
    t = Tablero(15)
    v = t.obtener_vehiculo('AvionCaza')
    p = t.obtener_posiciones(v, (0, 0), 'horizontal')
    ps = t.posicionar('AvionExplorador', (0, 1), 'horizontals')
    ps = t.posicionar('AvionExplorador', (0, 100), 'horizontal')
    ps = t.posicionar('AvionExploradors', (0, 1), 'horizontal')
    ps = t.posicionar('AvionExplorador', (0, 1), 'horizontal')
    ps = t.posicionar('AvionExplorador', (0, 1), 'horizontal')
    ps = t.posicionar('BuqueDeGuerra', (14, 1), 'horizontal')
    print(t.aereos['AvionExplorador'].posiciones_actuales)
    print(t)
