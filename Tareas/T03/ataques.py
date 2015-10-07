class Ataque:

    def __init__(self):
        self.usos = 0
        self.exitos = 0

    pass


class MisilTrident(Ataque):

    '''Misil UGM-133 Trident II'''
    # Todos los vehiculos, 5 puntos, un casillero.

    def __init__(self):
        super().__init__()
        self.area = (1, 1)
        self.dano = 5
        self.recoil = 0
        self.last_used = 0

    @property
    def disponible(self):
        return self._disponible


class MisilTomahawk(Ataque):
    pass

    '''Misil de crucero BGM-109 Tomahawk'''

    # 5 a una fila entera (hori o verti), notifica la cantidad de piezas atacadas, no la pos


class Napalm(Ataque):
    pass

    # Solo los Aviones Caza, dana 5 puntos a un casillero por dos turnos


class MisilBalistico(Ataque):
    pass

    '''Misil Balístico Intercontinental Minuteman III'''

    # Solo los Barcos Pequeños, una casilla, ataca 15.


class KamikazeIXXI(Ataque):
    pass

    # Solo los Aviones Kamikaze, destruye/autodestruye.


class GBUParalizer(Ataque):
    pass

    '''GBU-43/B Massive Ordenance Air Blast Paralizer'''

    # Contra el explorador. Dos casillas deben acertar. Lo paraliza por 5 turnos.


class KitDeIngenieros(Ataque):
    pass

    # Disminuir en 1 el daño de un vehiculo de la flota propia.