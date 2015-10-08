class Ataque:

    def __init__(self):
        self.usos = 0
        self.exitos = 0
        self.recoil = 0
        self.recoil_actual = 0

    @property
    def disponible(self):
        return self.recoil_actual == 0

    def atacar(self, receptor):
        destruido = receptor.recibir_ataque(self)
        self.exitos += 1
        self.usos += 1
        self.recoil_actual += self.recoil
        return destruido


class MisilTrident(Ataque):

    '''Misil UGM-133 Trident II'''
    # Todos los vehiculos, 5 puntos, un casillero.

    def __init__(self):
        super().__init__()
        self.area = (1, 1)
        self.dano = 5
        self.letra = 'T'


class MisilTomahawk(Ataque):

    '''Misil de crucero BGM-109 Tomahawk'''
    # 5 a una fila entera (hori o verti), notifica la cantidad de piezas atacadas, no la pos

    def __init__(self):
        super().__init__()
        self.area = (1, 1000)
        self.dano = 5
        self.letra = 'H'
        self.recoil = 3

    def generar_posiciones(self, inicial, tablero):
        vertical = [(i, inicial[1]) for i in range(tablero.n)]
        horizont = [(inicial[0], i) for i in range(tablero.n)]
        return {'V': vertical, 'H': horizont}


class Napalm(Ataque):

    # Solo los Aviones Caza, dana 5 puntos a un casillero por dos turnos

    def __init__(self):
        super().__init__()
        self.area = (1, 1)
        self.dano = 5
        self.letra = 'N'
        self.recoil = 8


class MisilBalistico(Ataque):

    '''Misil Balístico Intercontinental Minuteman III'''
    # Solo los Barcos Pequeños, una casilla, ataca 15.

    def __init__(self):
        super().__init__()
        self.area = (1, 1)
        self.dano = 15
        self.letra = 'B'
        self.recoil = 3


class KamikazeIXXI(Ataque):

    # Solo los Aviones Kamikaze, destruye/autodestruye.

    def __init__(self):
        super().__init__()
        self.area = (1, 1)
        self.dano = float('inf')
        self.letra = 'K'
        self.recoil = float('inf')


class GBUParalizer(Ataque):

    '''GBU-43/B Massive Ordenance Air Blast Paralizer'''
    # Contra el explorador. Dos casillas deben acertar. Lo paraliza por 5 turnos.

    def __init__(self):
        super().__init__()
        self.area = (2, 1)
        self.dano = 0
        self.letra = 'P'


class KitDeIngenieros(Ataque):

    # Disminuir en 1 el daño de un vehiculo de la flota propia.

    def __init__(self):
        super().__init__()
        self.area = (1, 1)
        self.dano = -1
        self.letra = 'I'
        self.recoil = 2

    def sanar(self, tablero, posicion):
        try:
            receptor = tablero.maritimo[posicion[0]][posicion[1]]
        except IndexError:
            receptor = ' '
        print(receptor)
        if str(receptor) not in ['X', ' ']:
            if receptor.resistencia == receptor.__class__().resistencia:
                return None
            sanado = receptor.recibir_ataque(self)
            self.exitos += 1
            self.usos += 1
            return sanado
        return None


if __name__ == '__main__':
    class Tab:
        def __init__(self, n):
            self.n = n
    toma = MisilTomahawk()
    p = toma.generar_posiciones((1, 2), Tab(9))['V']
    print(p)
