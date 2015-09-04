# coding=utf-8
from pacmatico import Distribucion, Pacmatico

sistema = Pacmatico()


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
