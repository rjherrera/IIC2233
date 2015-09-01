# coding=utf-8


class Reporte:

    def __init__(self):
        self.pacientes = []

    def __getitem__(self, i):
        return self.pacientes[i]

    def __len__(self):
        return len(self.pacientes)

    def pacientes_por_color(self, color):
        return [i for i in self.pacientes if i.color == color]

    def __str__(self):
        return str(self.pacientes)

    def __iter__(self):
        return iter(self.pacientes)


class Paciente:

    def __init__(self, id_obj, ano_inicio, mes, dia,
                 color, hora, motivo_alta):
        self.ano_inicio = ano_inicio
        self.mes = mes
        self.dia = dia
        self.color = color
        self.hora = hora
        self.motivo_alta = motivo_alta
        self.id = id_obj

    def __str__(self):
        return ('%d\t%s\t%s\t%s\t%s\t%s\t%s' % (self.id, self.ano_inicio,
                self.mes, self.dia, self.color, self.hora, self.motivo_alta))

    def __repr__(self):
        return 'Paciente(%d, %s, %s)' % (self.id, self.ano_inicio, self.color)


def paciente():
    with open('Reporte.txt') as f:
        n = 0
        paciente = [n] + f.readline().strip('\n').split('\t')
        paciente = Paciente(*paciente)
        yield paciente
        while True:
            paciente = [n] + f.readline().strip('\n').split('\t')
            paciente = Paciente(*paciente)
            n += 1
            yield paciente



if __name__ == '__main__':
    reporte = Reporte()
    cont_amar = 0
    cont_azul = 0
    cont_nara = 0
    cont_rojo = 0
    cont_verde = 0
    gen = paciente()
    while cont_amar < 10 or cont_azul < 10 or cont_nara \
            < 10 or cont_rojo < 10 or cont_verde < 10:
        p = next(gen)
        if p.color == 'amarillo' and p.ano_inicio == '2013' and cont_amar < 10:
            reporte.pacientes.append(p)
            cont_amar += 1
        if p.color == 'azul' and p.ano_inicio == '2013' and cont_azul < 10:
            reporte.pacientes.append(p)
            cont_azul += 1
        if p.color == 'naranja' and p.ano_inicio == '2013' and cont_nara < 10:
            reporte.pacientes.append(p)
            cont_nara += 1
        if p.color == 'rojo' and p.ano_inicio == '2013' and cont_rojo < 10:
            reporte.pacientes.append(p)
            cont_rojo += 1
        if p.color == 'verde' and p.ano_inicio == '2013' and cont_verde < 10:
            reporte.pacientes.append(p)
            cont_verde += 1
    print(reporte.pacientes_por_color('amarillo'))
