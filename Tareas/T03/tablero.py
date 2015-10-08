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
        self.posicionados = []
        self.historial_ataques = {}
        self.turno_actual = 0

    def __contains__(self, element):
        for i in range(self.n):
            if element in self.aereo[i] or element in self.maritimo[i]:
                return True
        return False

    def __str__(self):
        string = '\nMarítimo:'.ljust(self.n * 2) + '   :··: Aéreo:\n'  # es * 4
        for i in range(self.n):
            strs_mar = [str(i) for i in self.maritimo[i]]
            strs_air = [str(i) for i in self.aereo[i]]
            string += '|' + '|'.join(strs_mar) + '| :··: '  # espacios antes y dps
            string += '|' + '|'.join(strs_air) + '|\n'
        return string

    def asignar(self, lista, posicion, vehiculo):
        lista[posicion[0]][posicion[1]] = vehiculo

    def obtener_vehiculo(self, nombre_vehiculo):
        if nombre_vehiculo not in self.maritimos:
            if nombre_vehiculo not in self.aereos:
                raise KeyError('Vehiculo %r no encontrado.' % nombre_vehiculo)
            return self.aereos[nombre_vehiculo]
        return self.maritimos[nombre_vehiculo]

    def obtener_vehiculo_letra(self, letra_vehiculo):
        for key in self.maritimos:
            if self.maritimos[key].letra == letra_vehiculo:
                return self.maritimos[key]
        for key in self.aereos:
            if self.aereos[key].letra == letra_vehiculo:
                return self.aereos[key]
        raise KeyError('Vehiculo %r no encontrado.' % letra_vehiculo)

    def obtener_vehiculo_unico(self, letra_vehiculo):
        vehiculo = self.obtener_vehiculo_letra(letra_vehiculo)
        if vehiculo.letra not in self:
            return vehiculo
        raise KeyError('Vehículo %s ya posicionado.' % repr(vehiculo))

    def obtener_posiciones(self, vehiculo, posicion, orientacion):
        posiciones = vehiculo.generar_posiciones(posicion)[orientacion]
        vehiculo.orientacion = orientacion
        return posiciones

    def verificar_posiciones(self, posiciones, tablero):
        for pos in posiciones:
            try:
                tablero[pos[0]][pos[1]]
            except IndexError:
                return False, pos
        return True, None

    def verificar_disponibles(self, posiciones, tablero):
        for pos in posiciones:
            if tablero[pos[0]][pos[1]] != ' ':
                return False, pos
        return True, None

    def verificar_disponibles_mov(self, posiciones, tablero, vehiculo):
        for pos in posiciones:
            casillero = tablero[pos[0]][pos[1]]
            if casillero != ' ' and casillero != vehiculo.letra:
                return False, pos
        return True, None

    def posicionar(self, vehiculo, posiciones):
        try:
            tablero = self.maritimo
            if vehiculo.__class__ in self.__class__.aereos:
                tablero = self.aereo
            verificacion = self.verificar_posiciones(posiciones, tablero)
            if verificacion[0]:
                disponibles = self.verificar_disponibles(posiciones, tablero)
                if disponibles[0]:
                    for pos in posiciones:
                        self.asignar(tablero, pos, vehiculo)
                    self.posicionados.append(vehiculo)
                else:
                    pos = disponibles[1]
                    raise IndexError('está usado por otro vehículo.')
            else:
                pos = verificacion[1]
                raise IndexError('se encuentra fuera de rango.')
            vehiculo.posiciones_actuales = posiciones
        except (KeyError, ValueError, TypeError) as err:
            print(err.args[0])
        except IndexError as err:
            print('%r %s' % (pos, err.args[0]))

    def revisar_hundidos(self):
        for i in range(len(self.maritimo)):
            for j in range(len(self.maritimo)):
                if str(self.maritimo[i][j]) == 'X':
                    self.maritimo[i][j] = ' '

    def pasar_turno(self):
        for i, j in self.maritimos.items():
            for k, l in j.ataques.items():
                if l.recoil_actual:
                    l.recoil_actual -= 1

    @property
    def letras_vehiculos(self):
        string = '\nVehículos disponibles ("Letra: Nombre (Área)"):\n'
        string += 'Mar:'.ljust(30) + 'Aire:\n '
        lm = [(j.letra, i, j.area) for i, j in self.maritimos.items()]
        la = [(j.letra, i, j.area) for i, j in self.aereos.items()]
        for i in range(len(lm) - 1):
            string += ('%s: %s %r' % (lm[i][0], lm[i][1], lm[i][2])).ljust(30)
            string += '%s: %s %r\n ' % (la[i][0], la[i][1], la[i][2])
        string += '%s: %s %r' % (lm[-1][0], lm[-1][1], lm[-1][2])
        return string

    # def distribuir(self):
    #     while len(self.posicionados) < 7:
    #         print(self.letras_vehiculos)
    #         print(self)
    #         vehiculo = input('Elija un vehiculo para posicionar (Ej: \'B\'): ')
    #         try:
    #             vehiculo = self.obtener_vehiculo_unico(vehiculo)
    #         except KeyError as error:
    #             print(error.args[0])
    #             continue
    #         posicion = input('Elija coordenadas para el vehículo (Ej: 0, 1): ')
    #         posicion = posicion.replace(' ', '')
    #         orientacion = input('Elija una orientacion (H/V): ').upper()
    #         try:
    #             posiciones = self.obtener_posiciones(vehiculo,
    #                                                  posicion,
    #                                                  orientacion)
    #         except (KeyError, TypeError) as error:
    #             print(error.args[0])
    #             continue
    #         self.posicionar(vehiculo, posiciones)


if __name__ == '__main__':
    t = Tablero(15)
    v = t.obtener_vehiculo('AvionCaza')
    v1 = t.obtener_vehiculo('AvionExplorador')
    v = t.obtener_vehiculo('BuqueDeGuerra')
    p = t.obtener_posiciones(v, '0,1', 'H')
    p1 = t.obtener_posiciones(v, '6,0', 'H')
    p2 = t.obtener_posiciones(v, '0,100', 'H')
    p3 = t.obtener_posiciones(v, '14,1', 'H')
    ps = t.posicionar(v, p)
    ps = t.posicionar(v, p1)
    ps = t.posicionar(v, p2)
    ps = t.posicionar(v, p)
    ps = t.posicionar(v, p)
    ps = t.posicionar(v, p)
    ps = t.posicionar(v1, p3)
    print(t.letras_vehiculos)
    print(t)
    print(id(t.maritimo[0][2]), repr(t.maritimo[0][2]))
    print(id(t.maritimo[0][1]), repr(t.maritimo[0][1]))
