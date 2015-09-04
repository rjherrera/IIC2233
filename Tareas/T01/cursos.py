# coding=utf-8
import parser as lector


TIPO_ABREV = [('Cátedra', '(CAT)'), ('Ayudantía', '(AYD)'),
              ('Laboratorio', '(LAB)')]


class Curso:

    def __init__(self, nombre, sigla, NRC, campus, profesor,
                 seccion, creditos, capacidad, horarios,
                 aprobacion=False, retiro=True, ingles=False):
        self.nombre = nombre
        self.sigla = sigla
        self.NRC = NRC
        self.retiro = retiro
        self.ingles = ingles
        self.seccion = seccion
        self.aprobacion = aprobacion
        self.profesor = profesor if type(profesor) == list else [profesor]
        self.campus = campus
        self.creditos = creditos
        self.capacidad = capacidad
        self.horarios = horarios
        self.alumnos = []
        self.evaluaciones = []
        self.requisitos = ''

    @property
    def ocupados(self):
        return len(self.alumnos)

    @property
    def disponibles(self):
        return self.capacidad - self.ocupados

    def agregar_prueba(self, evaluacion):
        self.evaluaciones.append(evaluacion)
        return True

    def es_tomable(self):
        return self.disponibles > 0

    def agregar_alumno(self, alumno):
        self.alumnos.append(alumno)

    def remover_alumno(self, alumno):
        self.alumnos.remove(alumno)

    def __eq__(self, curso):
        return self.NRC == curso.NRC

    def __str__(self):
        return '%s-%d @ %r' % (self.sigla, self.seccion, self.horarios)

    def __repr__(self):
        return 'Curso(%s-%d)' % (self.sigla, self.seccion)


class Horario:

    def __init__(self, tipo, sala, modulos=[]):
        self.modulos = modulos
        self.tipo = tipo
        self.sala = sala
        abrev = [j for i, j in TIPO_ABREV if i == tipo]
        self.abreviacion = abrev[0] if len(abrev) != 0 else ''

    def __str__(self):
        counter_hora = 1
        counter_dia = 1
        initial = self.modulos[0]
        for modulo in self.modulos[1:]:
            if modulo.modulo == initial.modulo:
                counter_hora += 1
        for modulo in self.modulos[1:]:
            if modulo.dia == initial.dia:
                counter_dia += 1
        if counter_hora == len(self.modulos):
            string = '-'.join([i.dia for i in self.modulos])
            return string + ':%d' % self.modulos[0].modulo + self.abreviacion
        elif counter_dia == len(self.modulos):
            string = ','.join([str(i.modulo) for i in self.modulos])
            return '%s:' % initial.dia + string + self.abreviacion
        return ';'.join([str(i) for i in self.modulos]) + self.abreviacion

    def str_b(self, curso):
        string = '%s-%d %s' % (curso.sigla, curso.seccion, self.abreviacion)
        return string if len(string) != 14 else string + ' '

    def __repr__(self):
        string = str(self)[:str(self).find('(')]
        return 'Horario(%s)' % string


class Modulo:

    modulo_hora = [(1, '08:30'), (2, '10:00'), (3, '11:30'), (4, '14:00'),
                   (5, '15:30'), (6, '17:00'), (7, '18:30'), (8, '20:00')]

    def __init__(self, dia, modulo):
        self.dia = dia
        self.modulo = modulo
        hora = [j for i, j in self.__class__.modulo_hora if i == modulo]
        self.hora = hora[0] if len(hora) != 0 else ''

    def __str__(self):
        return '%s:%d' % (self.dia, self.modulo)

    def __repr__(self):
        return 'Modulo(%s)' % (self)

    def __hash__(self):
        return hash(self.dia + str(self.modulo))

    def __eq__(self, modulo):
        return self.dia + str(self.modulo) == modulo.dia + str(modulo.modulo)


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

    def __str__(self):
        return '%s: %s' % (self.tipo, self.fecha)


if __name__ == '__main__':

    courses = lector.CourseReader('cursos.txt')
    cursos = []

    for course in courses.dictionaries:
        horarios = []
        if course['hora_cat'] and course['sala_cat']:
            modulos = lector.process_hora(course['hora_cat'])
            modulos = [Modulo(i, int(j)) for i, j in modulos]
            h_cat = Horario(tipo='Cátedra',
                            sala=course['sala_cat'],
                            modulos=modulos)
            horarios.append(h_cat)
        if course['hora_lab'] and course['sala_lab']:
            modulos = lector.process_hora(course['hora_lab'])
            modulos = [Modulo(i, int(j)) for i, j in modulos]
            h_lab = Horario(tipo='Laboratorio',
                            sala=course['sala_lab'],
                            modulos=modulos)
            horarios.append(h_lab)
        if course['hora_ayud'] and course['sala_ayud']:
            modulos = lector.process_hora(course['hora_ayud'])
            modulos = [Modulo(i, int(j)) for i, j in modulos]
            h_ayud = Horario(tipo='Ayudantía',
                             sala=course['sala_ayud'],
                             modulos=modulos)
            horarios.append(h_ayud)
        c = Curso(nombre=course['curso'],
                  sigla=course['sigla'],
                  NRC=course['NRC'],
                  retiro=course['retiro'],
                  ingles=course['eng'],
                  seccion=course['sec'],
                  aprobacion=course['apr'],
                  profesor=course['profesor'],
                  campus=course['campus'],
                  creditos=course['cred'],
                  capacidad=course['ofr'],
                  horarios=horarios)
        cursos.append(c)
    print(len(cursos))
    for i in cursos[:300]:
        print(i)
    e1 = Evaluacion('IIC1103', 'I1', 3, '1-09')
    e2 = Evaluacion('', '', '', '1-09')
    e3 = Evaluacion('', '', '', '2-09')
    e4 = Evaluacion('', '', '', '1-09')

    l = [e1, e2]
    l2 = [e3, e4]
    print(set(l).intersection(set(l2)))
