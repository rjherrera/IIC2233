# coding=utf-8
from loader import usuarios, cursos, Alumno, Profesor
from datetime import datetime, timedelta
from pacmatico import Distribucion, Pacmatico

sistema = Pacmatico()


class MenuAlumnoBummer:

    def __init__(self, alumno, cursos):
        self.cursos = cursos
        self.alumno = alumno
        self.opciones = {
            '1': self.inscribir_ramo,
            '2': self.botar_ramo,
            '3': self.generar_horario,
            '4': self.generar_calendario
        }
        self.hora = '00:00'
        self.timestamp = datetime.utcnow()

    def mostrar(self):
        print('\nMenu Alumno:\n  ',
              '1: Inscribir ramo\n  ',
              '2: Botar ramo\n  ',
              '3: Generar horario\n  ',
              '4: Generar calendario de evaluaciones\n  ',
              '5: Salir (Desloguearse)\n')

    def ejecutar(self):
        while True:
            self.mostrar()
            eleccion = input('Ingrese una opcion: ')
            if eleccion == '5':
                return
            accion = self.opciones.get(eleccion)
            if accion:
                accion()
            else:
                print('%s no es una de las opciones, pruebe de nuevo.'
                      % eleccion)

    def pedir_horario(self):
        using_delta = datetime.utcnow() - self.timestamp
        if self.hora != '00:00' and using_delta < timedelta(minutes=3):
            if self.alumno.esta_en_horario(self.hora):
                return True
        hora = input('Ingrese la hora actual (Ej: 19:23): ')
        try:
            if self.alumno.esta_en_horario(hora):
                self.hora = hora
                self.timestamp = datetime.utcnow()
                return True
            else:
                print('No está en su horario de inscripción.')
                return False
        except:
            print('El formato de hora no se condice con "HH:MM"',
                  'como por ejemplo "23:12"')
            return self.pedir_horario()

    def inscribir_ramo(self):
        if self.pedir_horario():
            print('\nPara inscribir un ramo debe ingresar la sigla seguida',
                  'de la seccion. Para volver atrás puede escribir',
                  '"atras" o "volver".\n')
            while True:
                sigla = input('Ingrese sigla (Ej: MAT1630-1)[sigla/volver]: ')
                sigla = sigla.replace('-', '').upper()
                if sigla in self.cursos:
                    curso = self.cursos[sigla]
                    print('El ramo escogido corresponde a %s' % curso)
                    confirmacion = input('¿Desea inscribirlo? [s/n]: ')
                    if confirmacion in ['si', 's']:
                        self.alumno.tomar_curso(curso)
                elif sigla in ['ATRAS', 'Q', 'SALIR', 'S', 'VOLVER', 'V']:
                    break
                else:
                    print('El ramo solicitado no se ha encontrado,',
                          'pruebe de nuevo.')

    def botar_ramo(self):
        if self.pedir_horario():
            print('\nPara botar un ramo debe ingresar la sigla seguida',
                  'de la seccion. Para volver atrás puede escribir',
                  '"atras" o "volver".\n')
            ramos = ['%s-%s' % (i.sigla, i.seccion) for
                     i in self.alumno.cursos_por_tomar]
            print('Tus cursos tomados son: %r' % ramos)
            while True:
                sigla = input('Ingrese uno de sus ramos (Ej: MAT1630-1): ')
                sigla = sigla.replace('-', '').upper()
                if sigla in self.cursos:
                    curso = self.cursos[sigla]
                    print('El ramo escogido corresponde a %s' % curso)
                    confirmacion = input('¿Desea botarlo? [s/n]: ').lower()
                    if confirmacion in ['si', 's']:
                        self.alumno.botar_curso(curso)
                elif sigla in ['ATRAS', 'Q', 'SALIR', 'S', 'VOLVER', 'V']:
                    break
                else:
                    print('El ramo a botar no se ha encontrado,',
                          'pruebe de nuevo')

    def generar_horario(self):
        dicc = self.alumno.obtener_horarios()
        lista_filas = []
        dias = 'LMWJV'
        for k in range(1, 9):
            fila = [j[k] for j in [dicc[i] for i in dias]]
            lista_filas.append(fila)
        strings = [' | '.join(i) + ' |' for i in lista_filas]
        strings.insert(3, ' ' * 40 + 'ALMUERZO' + ' ' * 40 + '|')
        horas = ['08:30', '10:00', '11:30', '13:00', '14:00',
                 '15:30', '17:00', '18:30', '20:00']
        string = '\nHorario:\n\n'
        head = ' ' * 6 + '|'
        for i in dias:
            head += ' ' * 8 + i + ' ' * 8 + '|'
        string += head
        string += '\n' + '-' * 97
        for i in range(len(strings)):
            string += '\n' + horas[i] + ' | ' + strings[i]
        print(string)
        confirmacion = input('\n¿Desea exportarlo?[s/n]: ').lower()
        if confirmacion in ['si', 's']:
            now = str(datetime.utcnow().timestamp()).replace('.', '')
            name = 'horario_' + now + '.txt'
            with open(name, 'w') as f:
                f.write(string[2:])
            print('Horario exportado satisfactoriamente en %s' % name)
        return string

    def generar_calendario(self):
        evals = [(i, i.evaluaciones) for i in self.alumno.cursos_por_tomar]
        string = '\nCalendario de evaluaciones:\n\n'
        for curso, evaluaciones in evals:
            string += '%s-%s: \n' % (curso.sigla, curso.seccion)
            for prueba in evaluaciones:
                string += '  %s\n' % prueba
            if not evaluaciones:
                string += '  Sin información\n'
            string += '\n'
        print(string)
        return string


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


class MenuAlumnoPacmatico:

    sistema = sistema

    def __init__(self, alumno, cursos):
        self.cursos = cursos
        self.alumno = alumno
        self.distribucion = Distribucion(alumno)
        self.opciones = {
            '1': self.agregar_ramos,
            '2': self.sacar_ramos,
            '3': self.distribuir_puntos,
            '4': self.calcular_optimo
        }

    def mostrar(self):
        print('\nMenu Alumno:\n  ',
              '1: Agregar ramos\n  ',
              '2: Sacar ramos\n  ',
              '3: Distribuir puntos\n  ',
              '4: Calcular resultado\n  ',
              '5: Salir (Desloguearse)\n')

    def ejecutar(self):
        while True:
            self.mostrar()
            eleccion = input('Ingrese una opcion: ')
            if eleccion == '5':
                return
            accion = self.opciones.get(eleccion)
            if accion:
                accion()
            else:
                print('%s no es una de las opciones, pruebe de nuevo.'
                      % eleccion)

    def agregar_ramos(self):
        print('\nPara agregar un ramo debe ingresar la sigla seguida',
              'de la seccion. Para volver atrás puede escribir',
              '"atras" o "volver".\n')
        while True:
            sigla = input('Ingrese sigla (Ej: MAT1630-1)[sigla/volver]: ')
            sigla = sigla.replace('-', '').upper()
            if sigla in self.cursos:
                curso = self.cursos[sigla]
                print('El ramo escogido corresponde a %s' % curso)
                confirmacion = input('¿Desea agregarlo? [s/n]: ')
                if confirmacion in ['si', 's']:
                    self.distribucion.agregar_ramo(curso)
            elif sigla in ['ATRAS', 'Q', 'SALIR', 'S', 'VOLVER', 'V']:
                break
            else:
                print('El ramo solicitado no se ha encontrado,',
                      'pruebe de nuevo.')

    def sacar_ramos(self):
        print('\nPara sacar un ramo debe ingresar la sigla seguida',
              'de la seccion. Para volver atrás puede escribir',
              '"atras" o "volver".\n')
        while True:
            sigla = input('Ingrese sigla (Ej: MAT1630-1)[sigla/volver]: ')
            sigla = sigla.replace('-', '').upper()
            if sigla in self.cursos:
                curso = self.cursos[sigla]
                print('El ramo escogido corresponde a %s' % curso)
                confirmacion = input('¿Desea sacarlo? [s/n]: ')
                if confirmacion in ['si', 's']:
                    self.distribucion.sacar_ramo(curso)
            elif sigla in ['ATRAS', 'Q', 'SALIR', 'S', 'VOLVER', 'V']:
                break
            else:
                print('El ramo solicitado no se ha encontrado,',
                      'pruebe de nuevo.')

    def distribuir_puntos(self):
        print('\nPara distribuir puntos debes elegir el ramo y',
              'luego los puntos. Para volver atrás puede escribir',
              '"atras" o "volver".\n')
        self.ver_distribucion()
        while True:
            sigla = input('Ingrese sigla (Ej: MAT1630-1)[sigla/volver]: ')
            sigla = sigla.replace('-', '').upper()
            if sigla in self.cursos:
                curso = self.cursos[sigla]
                print('El ramo escogido corresponde a %s' % curso)
                suma_restaurar = input('Desea sumar o restaurar puntos [s/r]: ')
                if suma_restaurar == 's':
                    pts = input('Puntos a sumarle: ')
                    if pts.isdigit():
                        self.distribucion.distribuir_mas(curso, int(pts))
                    else:
                        print('Por favor ingrese un número.')
                elif suma_restaurar == 'r':
                    self.distribucion.restaurar_dist()
            elif sigla in ['ATRAS', 'Q', 'SALIR', 'S', 'VOLVER', 'V']:
                break
            else:
                print('El ramo solicitado no se ha encontrado,',
                      'pruebe de nuevo.')
            self.ver_distribucion()

    def calcular_optimo(self):
        self.__class__.sistema.append(self.distribucion)
        self.__class__.sistema.distribuir_optimamente()
        print('Luego de la asignación tus ramos son:')
        for i in self.distribucion.dados:
            print(i)

    def ver_distribucion(self):
        print('\nLa distribucion actual es:')
        self.distribucion.ver()


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
        print('\nBienvenido a la toma de ramos.\n')
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


if __name__ == '__main__':
    MenuLogin().ejecutar()
