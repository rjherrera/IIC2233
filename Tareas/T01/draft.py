# coding=utf-8


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
        self.ocupados = 0
        self.horarios = horarios
        self.alumnos = []
        self.evaluaciones = []
        self.requisitos = []

    @property
    def disponibles(self):
        return self.capacidad - self.ocupados

    def __repr__(self):
        return '%s-%d | %r' % (self.sigla, self.seccion, self.horarios)


class Usuario:

    def __init__(self, nombre, apellido, usuario, contrasena):
        self.nombre = nombre
        self.apellido = apellido
        self.usuario = usuario
        self.contrasena = contrasena


class Alumno(Usuario):

    def __init__(self, horario_inscripcion):
        self.horario_inscripcion = horario_inscripcion
        self.cursos_aprobados = []
        self.cursos_por_tomar = []


class Profesor(Usuario):
    pass


class Modulo:

    def __init__(self, dia, hora):
        self.dia = dia
        self.hora = hora

    def __eq__(self, modulo):
        return self.dia == modulo.dia and self.hora == self.hora

    def __repr__(self):
        return '%s:%d' % (self.dia, self.hora)


class Horario:

    def __init__(self, tipo, sala, modulos):
        self.tipo = tipo
        self.modulos = modulos if type(modulos) == list else [modulos]
        self.sala = sala

    def __repr__(self):
        string = '-'.join([i.dia for i in self.modulos])
        return string + ':%d' % self.modulos[0].hora


class Evaluacion:
    pass


l = [Modulo(i, j) for i in 'LMWJV' for j in range(1, 9)]
catedra = Horario('Cátedra', 'B12', l[1::16])
lab = Horario('Laboratorio', 'B13', l[19])
ayud = Horario('Ayudantía', 'D101', l[9::16])
print(catedra.modulos, lab.modulos, ayud.modulos)

curso = Curso(nombre='Introducción a la Universidad',
              sigla='PUC0001',
              NRC=10012,
              retiro=True,
              ingles=False,
              seccion=1,
              aprobacion=False,
              profesor='Ignacio Sánchez',
              campus='San Joaquín',
              creditos=10,
              capacidad=100,
              horarios=[catedra, lab, ayud])

print(curso)
# print(curso.ocupados, curso.disponibles)
# curso.ocupados += 1
# print(curso.ocupados, curso.disponibles)
# for k in vars(curso).keys():
#     print(k, ':', vars(curso)[k])
