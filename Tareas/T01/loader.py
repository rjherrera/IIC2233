# coding=utf-8
import parser
from cursos import Modulo, Horario, Curso
from usuarios import Alumno, Profesor


## CURSOS
courses = parser.CourseReader('cursos.txt')
cursos = []

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
        h_ayud = Horario(tipo='Cátedra',
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
## CURSOS


## USUARIOS
## REVISAR TEMA NOMBRE / APELLIDO
users = parser.PeopleReader('personas.txt')
usuarios = []

for user in users.dictionaries:
    if user['alumno']:
        u = Alumno(idolos=user['idolos'],
                   aprobados=user['ramos_pre'],
                   nombre_completo=user['nombre'],
                   usuario=user['usuario'],
                   contrasena=user['clave'])
    else:
        u = Profesor(nombre_completo=user['nombre'],
                     usuario=user['usuario'],
                     contrasena=user['clave'])
    usuarios.append(u)
print(len(usuarios))
## REVISAR TEMA NOMBRE / APELLIDO
## USUARIOS

## EVALUACIONES



## EVALUACIONES
