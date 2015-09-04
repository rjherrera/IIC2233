# coding=utf-8
from loader.loader import usuarios, cursos, Alumno, Profesor
from menu.menu_pacmatico import MenuAlumnoPacmatico
from menu.menu_bummer import MenuAlumnoBummer


class MenuProfesor:

    def __init__(self, profesor, cursos, usuarios):
        self.cursos = cursos
        self.profesor = profesor
        self.usuarios = usuarios
        self.opciones = {
            '1': self.dar_permiso,
            '2': self.quitar_permiso,
        }

    def mostrar(self):
        print('\nMenu Profesor:\n  ',
              '1: Dar permiso\n  ',
              '2: Quitar permiso\n  ',
              '3: Salir\n  ')

    def ejecutar(self):
        while True:
            self.mostrar()
            eleccion = input('Ingrese una opcion: ')
            if eleccion == '3':
                return
            accion = self.opciones.get(eleccion)
            if accion:
                accion()
            else:
                print('%s no es una de las opciones, pruebe de nuevo.'
                      % eleccion)

    def dar_permiso(self):
        print('\nPara otorgar un permiso especial para un ramo debe',
              'ingresar la sigla seguida de la seccion. Luego debe ingresar',
              'un usuario al cual darle el permiso. Para volver atrás',
              'puede escribir "atras" o "volver".\n')
        while True:
            sigla = input('Ingrese sigla (Ej: ICS1113-1)[sigla/volver]: ')
            sigla = sigla.replace('-', '').upper()
            if sigla in self.cursos:
                curso = self.cursos[sigla]
                print('El ramo escogido corresponde a %s' % curso)
                alumno = input('Ingrese el nombre de usuario del alumno: ')
                if alumno in self.usuarios:
                    alumno = self.usuarios[alumno]
                    if type(alumno) == Alumno:
                        confirmacion = input('¿Desea dar el permiso? [s/n]: ')
                        if confirmacion in ['si', 's']:
                            self.profesor.dar_permiso(alumno, curso)
                            print('Permiso otorgado.')
                    else:
                        print('Le está intentando otorgar permiso a un profesor.')
                else:
                    print('Usuario no encontrado.')
            elif sigla in ['ATRAS', 'Q', 'SALIR', 'S', 'VOLVER', 'V']:
                break
            else:
                print('El ramo solicitado no se ha encontrado,',
                      'pruebe de nuevo.')

    def quitar_permiso(self):
        print('\nPara quitar un permiso especial para un ramo debe',
              'ingresar la sigla seguida de la seccion. Luego debe ingresar',
              'un usuario al cual quitarle el permiso. Para volver atrás',
              'puede escribir "atras" o "volver".\n')
        ramos = ['%s-%s a %s' % (j.sigla, j.seccion, i.usuario) for
                 i, j in self.profesor.permisos_dados]
        print('Tus persmisos otorgados son: %r' % ramos)
        while True:
            sigla = input('Ingrese sigla (Ej: ICS1113-1)[sigla/volver]: ')
            sigla = sigla.replace('-', '').upper()
            if sigla in self.cursos:
                curso = self.cursos[sigla]
                print('El ramo escogido corresponde a %s' % curso)
                alumno = input('Ingrese el nombre de usuario del alumno: ')
                if alumno in self.usuarios:
                    alumno = self.usuarios[alumno]
                    print('¡Alerta!: Esta acción le botará el curso',
                          'si el alumno ya lo tomó.')
                    confirmacion = input('¿Desea quitar el permiso? [s/n]: ')
                    if confirmacion in ['si', 's']:
                        self.profesor.quitar_permiso(alumno, curso)
                else:
                    print('Usuario no encontrado.')
            elif sigla in ['ATRAS', 'Q', 'SALIR', 'S', 'VOLVER', 'V']:
                break
            else:
                print('El ramo solicitado no se ha encontrado,',
                      'pruebe de nuevo.')


class MenuLogin:

    usuarios = usuarios

    def __init__(self):
        self.opciones = {
            '1': self.login,
        }

    def mostrar(self):
        print('\nMenu Ingreso:\n  ',
              '1: Ingresar\n  ',
              '2: Salir\n  ')

    def ejecutar(self):
        print('\nBienvenido a la toma de ramos.')
        while True:
            self.mostrar()
            eleccion = input('Ingrese una opcion: ')
            if eleccion == '2':
                print('Adiós')
                return
            accion = self.opciones.get(eleccion)
            if accion:
                accion()
            else:
                print('%s no es una de las opciones, pruebe de nuevo.'
                      % eleccion)

    def bummer_pacmatico(self, usuario):
        if type(usuario) == Profesor:
            return MenuProfesor
        print('\n¿Cómo está el día?:\n  ',
              '1: Caluroso\n  ',
              '2: Tibio\n  ',
              '3: Fresco\n  ',
              '4: Frío\n  ',
              '*: Otro\n  ')
        estado = input('Ingrese una opcion: ')
        if estado in ['2', '3']:
            print('\nBienvenido a Bummer.')
            return MenuAlumnoBummer
        else:
            print('\nBummer solo funciona en condiciones favorables.')
            print('\nBienvenido a Pacmático.')
            return MenuAlumnoPacmatico

    def login(self):
        usuario = input('Ingrese su nombre de usuario: ')
        if usuario in MenuLogin.usuarios:
            tries = 0
            usuario = MenuLogin.usuarios[usuario]
            while tries < 5:
                clave = input('Ingrese su contraseña: ')
                if usuario.ingresar(clave):
                    sistema = self.bummer_pacmatico(usuario)
                    if sistema == MenuProfesor:
                        sistema(usuario, cursos, usuarios).ejecutar()
                    else:
                        sistema(usuario, cursos).ejecutar()
                    print('Te has desconectado.')
                    break
                else:
                    print('Contraseña incorrecta.')
                    tries += 1
            if tries == 5:
                print('Has agotado tus intentos.')
        else:
            print('Usuario no encontrado.')


# if __name__ == '__main__':
#     MenuLogin().ejecutar()
