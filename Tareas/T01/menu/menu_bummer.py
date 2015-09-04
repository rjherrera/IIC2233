# coding=utf-8
from datetime import datetime, timedelta


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
                self.alertar()
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
            name = 'files/horario_' + now + '.txt'
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

    def alertar(self):
        if self.alumno.creditos < 30:
            print('¡Vas a salir del sistema con menos de 30 créditos!')
