# coding=utf-8
from requisitos import cumple as pasa_requisito


class Usuario:

    def __init__(self, nombre_completo, usuario, contrasena):
        self.nombre_completo = nombre_completo
        self.usuario = usuario
        self.contrasena = contrasena


class Alumno(Usuario):

    def __init__(self, idolos, aprobados, **kwargs):
        super().__init__(**kwargs)
        # self.horario_inscripcion = horario_inscripcion
        self.creditos_maximos = 60  # cambiar!
        self._cursos_aprobados = aprobados
        self.idolos = idolos
        self.cursos_por_tomar = []
        self.permisos = []

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

    def tope_evaluaciones(self, curso):
        mis_evaluaciones = set(self.evaluaciones)
        pruebas_curso = set(curso.evaluaciones)
        return bool(mis_evaluaciones.intersection(pruebas_curso))

    def tomar_curso(self, curso):
        if self.creditos + curso.creditos > self.creditos_maximos:
            print('De tomar este ramo excederías tu máximo de créditos.')
            return False
        if self.tope_evaluaciones(curso):
            print('Te topan las evaluaciones con alguno de tus ramos')
            return False
        if not curso.aprobacion:
            if (pasa_requisito(self.cursos_aprobados, curso.requisitos)
                    or curso in self.permisos):
                self.agregar_curso(curso)
                return True
            print('No cumples con los requisitos.')
        else:
            if curso in self.permisos:
                if curso.es_tomable():
                    self.agregar_curso(curso)
                    return True
                print('No hay cupos disponibles.')
            print('El curso requiere aprobación.')
        return False

    def agregar_curso(self, curso):
        self.cursos_por_tomar.append(curso)
        self.cursos_aprobados.append(curso.sigla + '[c]')


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


if __name__ == '__main__':
    p = Profesor(nombre_completo='', usuario='', contrasena='')
