# coding=utf-8
import parser
from cursos import Modulo, Horario, Curso
from usuarios import Alumno, Profesor
from evaluaciones import Evaluacion
from bacanosidad import bacanosidad_grupo


# REQUISITOS
# print('Creando requisitos...')
requirements = parser.RequirementsReader('requisitos.txt')
requisitos = {}

for requirement in requirements.dictionaries:
    # eqs = requirement['equiv'][1:-1] # por situación asumida en desuso
    # equivs = eqs.split('o') if requirement['equiv'] != 'Notiene' else []
    prerreq = parser.process_req(requirement['prerreq'])
    # requisitos[requirement['sigla']] = (equivs, prerreq)
    requisitos[requirement['sigla']] = prerreq
# print('Requisitos creados.')
# REQUISITOS
# print()
# CURSOS
# print('Creando cursos...')
courses = parser.CourseReader('cursos.txt')
cursos = {}

for course in courses.dictionaries:
    horarios = []
    if course['hora_cat'] and course['sala_cat']:
        modulos = parser.process_hora(course['hora_cat'])
        modulos = [Modulo(i, int(j)) for i, j in modulos]
        h_cat = Horario(tipo='Cátedra',
                        sala=course['sala_cat'],
                        modulos=modulos)
        horarios.append(h_cat)
    if course['hora_lab'] and course['sala_lab']:
        modulos = parser.process_hora(course['hora_lab'])
        modulos = [Modulo(i, int(j)) for i, j in modulos]
        h_lab = Horario(tipo='Laboratorio',
                        sala=course['sala_lab'],
                        modulos=modulos)
        horarios.append(h_lab)
    if course['hora_ayud'] and course['sala_ayud']:
        modulos = parser.process_hora(course['hora_ayud'])
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
    if c.sigla in requisitos:
        c.requisitos = requisitos[c.sigla]
    cursos[course['sigla'] + str(course['sec'])] = c
# print('Cursos creados.')
# CURSOS
# print()
# USUARIOS
# print('Creando usuarios...')
users = parser.PeopleReader('personas.txt')
usuarios = {}

for user in users.dictionaries:
    if user['alumno']:
        aprobados = user['ramos_pre'] + ['']
        u = Alumno(idolos=user['idolos'],
                   aprobados=aprobados,
                   nombre_completo=user['nombre'],
                   usuario=user['usuario'],
                   contrasena=user['clave'])
    else:
        u = Profesor(nombre_completo=user['nombre'],
                     usuario=user['usuario'],
                     contrasena=user['clave'])
    usuarios[u.usuario] = u
# print('Usuarios creados.')
# USUARIOS
# print()
# EVALUACIONES
# print('Asignando evaluaciones a los cursos...')
tests = parser.TestsReader('evaluaciones.txt')
evaluaciones = []
for test in tests.dictionaries:
    sigla = test['sigla']
    e = Evaluacion(sigla=sigla,
                   tipo=test['tipo'],
                   seccion=test['sec'],
                   fecha=test['fecha'])
    evaluaciones.append(e)
# ASIGNAR EVALUACIONES
for prueba in evaluaciones:
    if (prueba.sigla + str(prueba.seccion)) in cursos:
        cursos[prueba.sigla + str(prueba.seccion)].agregar_prueba(prueba)
# print('Evaluaciones asignadas.')
# EVALUACIONES
# print()
# BACANOSIDAD
# print('Asignando usuarios a sus grupos...')
for user, b_relativa, grupo in bacanosidad_grupo:
    for usuario in usuarios.values():
        if usuario.nombre_completo == user:
            usuario.bacanosidad_relativa = b_relativa
            usuario.horario_inscripcion = grupo
# print('Usuarios asignados.')
# BACANOSIDAD


if __name__ == '__main__':
    print()
    print(len(requisitos))
    print(len(cursos))
    print(len(usuarios))
    print(len(evaluaciones))
    print(usuarios['msmith2'].ingresar('Z9GksEBxs'))
    # print(usuarios['msmith2'].cursos_aprobados)
    # print(cursos['MAT16403'].requisitos)
