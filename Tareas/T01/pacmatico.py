# coding=utf-8


class Distribucion:

    def __init__(self, alumno):
        self.alumno = alumno
        self.ramos = []
        self.dados = []
        self.ramos_distribuidos = []
        self.distribuidos = 0
        self.cred_red = 0

    @property
    def puntos(self):
        return sum([i[1] for i in self.dados])

    def agregar_ramo(self, ramo):
        self.ramos.append([ramo, 0])
        self.update_eq_points()

    def sacar_ramo(self, ramo_ext):
        presente = False
        for ramo, pts in self.ramos:
            if ramo == ramo_ext:
                presente = True
        if presente:
            self.ramos.remove([ramo_ext, pts])
        self.update_eq_points()

    def update_eq_points(self):
        if len(self.ramos) > 0:
            pts = self.alumno.puntos_pacmatico / len(self.ramos)
        else:
            pts = self.alumno.puntos_pacmatico
        for ramo_puntos in self.ramos:
            ramo_puntos[1] = pts
        self.cred_red = 0

    def distribuir_mas(self, ramo, puntos):
        if len(self.ramos) > 1:
            if self.distribuidos + puntos < 1000:
                if self.cred_red <= 45:
                    for ramo_puntos in self.ramos:
                        if ramo_puntos[0] == ramo:
                            ramo_puntos[1] += puntos
                            self.distribuidos += puntos
                            if ramo not in self.ramos_distribuidos:
                                self.cred_red += ramo.creditos
                                self.ramos_distribuidos.append(ramo)
                        else:
                            ramo_puntos[1] -= puntos / (len(self.ramos) - 1)
                else:
                    print('No puedes redistribuir más de 45 créditos.')
            else:
                print('Te has excedido del máximo (1000 pts redistribuidos).')
        else:
            print('Necesitas al menos 2 ramos para redistribuir.')

    def restaurar_dist(self):
        self.update_eq_points()

    def ver(self):
        for i, j in self.ramos:
            print('%s-%s: %s' % (i.sigla, i.seccion, j))
        print()


class Pacmatico:

    def __init__(self):
        self.distribuciones = []

    def distribuir_optimamente(self):
        for ramo in self.obtener_ramos():
            for alumno, curso, puntos, dist in ramo:
                if alumno.agregar_curso(curso):
                    dist.dados.append(curso)

    def obtener_ramos(self):
        dicc = {}
        for dist in self.distribuciones:
            for i, j in dist.ramos:
                if i.sigla in dicc:
                    dicc[i.sigla] += [(dist.alumno, i, j, dist)]
                else:
                    dicc[i.sigla] = [(dist.alumno, i, j, dist)]
        for ramo in dicc:
            ramo.sort(key=lambda x: x[2])
        return dicc
