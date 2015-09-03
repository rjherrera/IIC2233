# coding=utf-8


class Evaluacion:

    def __init__(self, sigla, tipo, seccion, fecha):
        self.sigla = sigla
        self.tipo = tipo
        self.seccion = seccion
        self.fecha = fecha

    def __eq__(self, evaluacion):
        if self.fecha != 'NA':
            return self.fecha == evaluacion.fecha
        return False

    def __hash__(self):
        return hash(self.fecha)

    def __repr__(self):
        return 'Evaluacion(%s-%s - %s)' % (self.tipo, self.sigla, self.fecha)

if __name__ == '__main__':
    pass
    e1 = Evaluacion('IIC1103', 'I1', 3, '1-09')
    e2 = Evaluacion('', '', '', '1-09')
    e3 = Evaluacion('', '', '', '2-09')
    e4 = Evaluacion('', '', '', '1-09')

    l = [e1, e2]
    l2 = [e3, e4]
    print(set(l).intersection(set(l2)))
