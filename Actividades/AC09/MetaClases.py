def check_creator(self):
    if self.creador in self.creadores:
        print('El creador está en la lista de programadores')
        return True
    print('El creador no está en la lista de programadores')
    return False


def cortar_conexion(self):
    if self.actual.hacker:
        self.actual.hacker = 0
        print('Hay un hacker en el puerto, se cortó la conexión')
    else:
        print('No hay hacker')


def cambiar_nodo(self, nodo):
    print('Cambiando desde el nodo %s a el nodo %s' % (self.actual.ide, nodo.ide))
    self.actual = nodo


class MetaRobot(type):

    def __new__(meta, nombre, base_clases, diccionario):
        diccionario['creador'] = 'rjherrera'
        diccionario['ip_inicio'] = '190.102.62.283'
        diccionario['check_creator'] = check_creator
        diccionario['cortar_conexion'] = cortar_conexion
        diccionario['cambiar_nodo'] = cambiar_nodo
        if nombre != 'Robot':
            raise NameError('Nombre no aceptado')
        return super().__new__(meta, nombre, base_clases, diccionario)
