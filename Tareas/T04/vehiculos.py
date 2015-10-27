from random import uniform, randint


class Auto:

    def __init__(self, sentido):
        self.velocidad = uniform(0.5, 1)
        self.taxi = True if randint(0, 9) > 7 else False
        self.ultimo_mov = 0
        self.sentido = sentido


class Emergencia:

    def __init__(self, sentido):
        self.velocidad = 1
        self.ultimo_mov = 0
        self.sentido = sentido
        self.sirena = True


class Ambulancia(Emergencia):

    pass


class Carro(Emergencia):

    pass


class Policia(Emergencia):

    pass