# coding=utf-8
from requisitos import cumple as pasa_requisito
from datetime import datetime


class Usuario:

    def __init__(self, nombre_completo, usuario, contrasena):
        self.nombre_completo = nombre_completo
        self.usuario = usuario
        self.__contrasena = contrasena

    def ingresar(self, contrasena):
        return self.__contrasena == contrasena


class Alumno(Usuario):

    horarios = [('8:30', '10:30'), ('9:30', '11:30'), ('10:30', '12:30'),
                ('11:30', '13:30'), ('12:30', '14:30'), ('13:30', '15:30'),
                ('14:30', '16:30'), ('15:30', '17:30'), ('16:30', '18:30'),
                ('17:30', '19:30')]

    def __init__(self, idolos, aprobados, **kwargs):
        super().__init__(**kwargs)
        self._horario_inscripcion = []
        self.bacanosidad_relativa = 0
        self._grupo = 0
        self._cursos_aprobados = aprobados
        self.idolos = idolos
        self.cursos_por_tomar = []
        self.permisos = []

    @property
    def creditos_maximos(self):
        return 55 + ((6 - self._grupo) * 2)

    @property
    def horario_inscripcion(self):
        return self._horario_inscripcion

    @horario_inscripcion.setter
    def horario_inscripcion(self, grupo):
        hora_inicio, hora_termino = Alumno.horarios[grupo - 1]
        inicio = datetime.strptime(hora_inicio, '%H:%M').time()
        termino = datetime.strptime(hora_termino, '%H:%M').time()
        self._horario_inscripcion = [inicio, termino]
        self._grupo = grupo

    @property
    def cursos_aprobados(self):
        correq = [i + '[c]' for i in self._cursos_aprobados]
        return self._cursos_aprobados + correq

    @property
    def creditos(self):
        return sum(i.creditos for i in self.cursos_por_tomar)

    @property
    def evaluaciones(self):
        evals_por_curso = [i.evaluaciones for i in self.cursos_por_tomar]
        return [j for i in evals_por_curso for j in i]

    def obtener_horarios(self):
        dflt = ' ' * 15
        dicc = dict((i, dict((j + 1, dflt) for j in range(8))) for i in 'LMWJV')
        for curso in self.cursos_por_tomar:
            for horario in curso.horarios:
                string = horario.str_b(curso)
                for modulo in horario.modulos:
                    dicc[modulo.dia][modulo.modulo] = string
        return dicc

    def esta_en_horario(self, hora):
        hora = datetime.strptime(hora, '%H:%M').time()
        inicio, termino = self.horario_inscripcion
        return hora >= inicio and hora <= termino

    def tope_evaluaciones(self, curso):
        mis_evaluaciones = set(self.evaluaciones)
        pruebas_curso = set(curso.evaluaciones)
        return bool(mis_evaluaciones.intersection(pruebas_curso))

    def tope_cat_lab(self, curso):
        mis_modulos = []
        for i in self.cursos_por_tomar:
            for horario in i.horarios:
                if horario.tipo != 'Ayudantía':
                    mis_modulos.extend(horario.modulos)
        cur_mods = [i.modulos for i in curso.horarios if i.tipo != 'Ayudantía']
        cur_mods = [j for i in cur_mods for j in i]
        return bool(set(cur_mods).intersection(set(mis_modulos)))

    def tope_campus(self, curso):
        campuses = [i.campus for i in self.cursos_por_tomar]
        if set(campuses) == set([curso.campus]):  # si es el mismo campus
            return False
        mis_modulos = []
        for i in self.cursos_por_tomar:
            for horario in i.horarios:
                if horario.tipo != 'Ayudantía':
                    mis_modulos.append((curso, horario.modulos))
        cur_mods = [i.modulos for i in curso.horarios if i.tipo != 'Ayudantía']
        cur_mods = [j for i in cur_mods for j in i]
        for i, j in mis_modulos:
            if i.campus != curso.campus:
                for k in j:
                    for l in cur_mods:
                        if abs(k.modulo - l.modulo) == 1:
                            return True
        return False

    def tomar_curso(self, curso):
        if self.tope_cat_lab(curso):
            print('No se pueden tomar cursos con tope de cátedras',
                  'ni de laboratorio con cátedra ni de laboratorios.')
            return False
        if self.tope_campus(curso):
            print('No se pueden tomar ramos consecutivos en campus distintos.')
            return False
        if self.tope_evaluaciones(curso):
            print('Te topan las evaluaciones con alguno de tus ramos.')
            return False
        if curso in self.cursos_por_tomar:
            print('El ramo se encuentra en tus ramos a cursar.')
            return False
        if self.creditos + curso.creditos > self.creditos_maximos:
            print('De tomar este ramo excederías tu máximo de créditos.')
            return False
        if not curso.aprobacion:
            if (pasa_requisito(self.cursos_aprobados, curso.requisitos)
                    or curso in self.permisos):
                self.agregar_curso(curso)
                print('Curso inscrito.')
                return True
            print('No cumples con los requisitos.')
        else:
            if curso in self.permisos:
                if curso.es_tomable():
                    self.agregar_curso(curso)
                    print('Curso inscrito.')
                    return True
                print('No hay cupos disponibles.')
            print('El curso requiere aprobación.')
        return False

    def botar_curso(self, curso):
        if self.creditos < 30:
            print('Al botar este ramo quedarás con menos de 30 créditos.')
        if curso in self.cursos_por_tomar:
            if curso.retiro:
                self.cursos_por_tomar.remove(curso)
                curso.remover_alumno(self)
                print('Curso retirado.')
                return True
            else:
                print('Curso no retirable.')
        else:
            print('No has tomado ese curso')
        return False

    def agregar_curso(self, curso):
        self.cursos_por_tomar.append(curso)
        self.cursos_aprobados.append(curso.sigla + '[c]')
        curso.agregar_alumno(self)

    def __repr__(self):
        return 'Alumno(%s, %s)' % (self.nombre_completo, self.usuario)


class Profesor(Usuario):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cursos_dictados = []
        self.permisos_dados = []

    def dicta_curso(self, curso):
        for profesor in curso.profesor:
            n_palabras = profesor.count(' ') + 1
            cuenta = 0
            for nombre in self.nombre_completo.split():
                if nombre in profesor.split():
                    cuenta += 1
            if n_palabras == cuenta:
                return True
        return False

    def dar_permiso(self, alumno, curso):
        if self.dicta_curso(curso):
            alumno.permisos.append(curso)
            self.permisos_dados.append((alumno, curso))
            return True
        return False

    def quitar_permiso(self, alumno, curso):
        if (alumno, curso) in self.permisos_dados or self.dicta_curso(curso):
            if curso in alumno.permisos:
                alumno.permisos.remove(curso)
            if curso in alumno.cursos_por_tomar:
                alumno.cursos_por_tomar.remove(curso)
            if (alumno, curso) in self.permisos_dados:
                self.permisos_dados.remove((alumno, curso))
            return True
        return False

    def __repr__(self):
        return 'Profesor(%s, %s)' % (self.nombre_completo, self.usuario)


if __name__ == '__main__':
    p = Profesor(nombre_completo='', usuario='', contrasena='')
