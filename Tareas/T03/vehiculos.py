from ataques import *


class Vehiculo:

    def __init__(self):
        self.posiciones_actuales = []
        self.movimientos = 0
        self.ataques_recibidos = 0
        self.dano_recibido = 0
        self.orientacion = 'H'

    def generar_posiciones(self, inicial):
        vertical = [(inicial[0] + i, inicial[1] + j)
                    for i in range(self.area[0]) for j in range(self.area[1])]
        horizont = [(inicial[0] + i, inicial[1] + j)
                    for i in range(self.area[1]) for j in range(self.area[0])]
        return {'V': vertical, 'H': horizont}

    def __str__(self):
        return self.__class__.__name__

    def recibir_ataque(self, ataque):
        self.ataques_recibidos += 1
        self.dano_recibido += ataque.dano
        self.resistencia -= ataque.dano


class BarcoPequeno(Vehiculo):

    # 3 × 1, 30, Misil Balistico Intercontinental c/3 turnos.

    def __init__(self):
        super().__init__()
        self.letra = 'b'
        self.resistencia = 30
        self.area = (3, 1)
        self.ataques = {'MisilBalistico': MisilBalistico(),
                        'MisilTrident': MisilTrident()}


class BuqueDeGuerra(Vehiculo):

    # 2 × 3, 60, Misil de crucero BGM-109 Tomahawk c/3 turnos

    def __init__(self):
        super().__init__()
        self.letra = 'B'
        self.resistencia = 60
        self.area = (3, 2)
        self.ataques = {'MisilTomahawk': MisilTomahawk(),
                        'MisilTrident': MisilTrident()}


class Lancha(Vehiculo):

    # 2 × 1, 1, no ataques, moverse todas las casillas que desee.

    def __init__(self):
        super().__init__()
        self.letra = 'L'
        self.resistencia = 1
        self.area = (2, 1)
        self.ataques = {}


class Puerto(Vehiculo):

    # 2 × 4, 80, permite reparar un vehiculo cada dos turnos. Estático

    def __init__(self):
        super().__init__()
        self.letra = 'P'
        self.resistencia = 80
        self.area = (4, 2)
        self.ataques = {}


class VehiculoAereo:

    pass


class AvionExplorador(Vehiculo):

    # 3 × 3, dada cierta area 3 × 3 por el jugador, notifica la existencia de un barco ahi
    # area. Su desventaja es que luego de explorar, existe un 50 % de probabilidad de

    def __init__(self):
        super().__init__()
        self.letra = 'E'
        self.area = (3, 3)
        self.ataques = {'MisilTrident': MisilTrident()}


class AvionKamikazeIXXI(Vehiculo):

    # 1 × 1, se le entrega coordenada, usa el ataque kamikaze

    def __init__(self):
        super().__init__()
        self.letra = 'K'
        self.area = (1, 1)
        self.ataques = {'KamikazeIXXI': KamikazeIXXI(),
                        'MisilTrident': MisilTrident()}


class AvionCaza(Vehiculo):

    # 1 × 1, utiliza Napalm, pero una vez cada ocho turnos.

    def __init__(self):
        super().__init__()
        self.letra = 'C'
        self.area = (1, 1)
        self.ataques = {'Napalm': Napalm(),
                        'MisilTrident': MisilTrident()}

if __name__ == '__main__':
    print(BuqueDeGuerra().generar_posiciones((0, 0)))
    print(AvionExplorador().generar_posiciones((0, 0)))
