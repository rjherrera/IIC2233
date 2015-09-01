# coding=utf-8


class Evaluacion:

    def __init__(self, sigla, tipo, seccion, fecha):
        self.sigla = sigla
        self.tipo = tipo
        self.seccion = seccion
        self.fecha = fecha

    def __eq__(self, evaluacion):
        return self.fecha == evaluacion.fecha

if __name__ == '__main__':
    pass
