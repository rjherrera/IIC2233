# coding=utf-8


class Usuario:

    def __init__(self, nombre_completo, usuario, contrasena):
        self.nombre_completo = nombre_completo
        self.usuario = usuario
        self.contrasena = contrasena

    # @property
    # def completo(self):
    #     return '%s %s' % (self.apellido, self.nombre)


class Alumno(Usuario):

    def __init__(self, idolos, aprobados, **kwargs):
        super().__init__(**kwargs)
        # self.horario_inscripcion = horario_inscripcion
        self.cursos_aprobados = aprobados
        self.idolos = idolos
        self.cursos_por_tomar = []
        self.permisos = []

    def tomar_curso(self, curso):
        pass


class Profesor(Usuario):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cursos_dictados = []
        self.permisos_dados = []

    def obtener_dictados(self, cursos):
        for curso in cursos:
            if self.completo in curso.profesor:
                self.cursos_dictados.append(curso)

    def dar_permiso(self, alumno, curso):
        if curso in self.cursos_dictados:
            alumno.permisos.append(curso)
            self.permisos_dados.append((alumno, curso))
            return True
        return False

    def quitar_permiso(self, alumno, curso):
        if ((alumno, curso) in self.permisos_dados
                or curso in self.cursos_dictados):
            if curso in alumno.permisos:
                alumno.permisos.pop(curso)
            if curso in alumno.cursos_por_tomar:
                alumno.cursos_por_tomar.pop(curso)
            self.permisos_dados.pop((alumno, curso))
            return True
        return False

if __name__ == '__main__':
    p = Profesor(nombre_completo='', usuario='', contrasena='')
