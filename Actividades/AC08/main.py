# coding=utf-8


def tipar(*tipos):
    def _tipar(function):
        def __tipar(*args, **kw):  # asumo que el orden importa para hacer zip
            if len(tipos) != len(args):
                print('Ha ingresado distinto número de argumentos y tipos')
            else:
                trues = 0
                for tipo, argumento in zip(tipos, args):
                    if isinstance(argumento, tipo):
                        trues += 1
                if trues == len(tipos):
                    return function(*args, **kw)
                else:
                    print('Los tipos no coinciden con los argumentos.')
        return __tipar
    return _tipar


class Overload:

    def __init__(self, func):
        self.funciones = [((), func)]
        # implementar este método para inicializar el decorador
        pass

    def overload(self, *tipos):
        def decorador(funcion):
            # self.funciones[tipos] = funcion
            self.funciones.append((tipos, funcion))
            return self
        return decorador
        # implementar este método para agregar nuevos overloads la
        # función original
        pass

    def __call__(self, *args, **kwargs):
        for i, j in self.funciones:
            l = tuple(type(k) for k in args[1:])
            if i == l:
                return j(*args)
        return self.funciones[0][1](self)


    # El siguiente método es para que puedan usar esta clase como
    # decorador desde otras clases. No deben modificar nada en él.
    def __get__(self, obj, cls):
        def caller(*args, **kwargs):
            return self(obj, *args, **kwargs)
        return caller


if __name__ == "__main__":

    @tipar(int, int)
    def suma(a, b):
        return a + b

    @tipar(str, str)
    def sumar_string(s1, s2):
        return s1 + ' ' + s2 + '!'

    @tipar(list, list, tuple)
    def sumar_lista(lista1, lista2, tupla):
        return lista1 + lista2 + list(tupla)

    class ClaseOverloaded:

        def __init__(self, nombre, edad, lista_cosas):
            self.nombre = nombre
            self.edad = edad
            self.lista_cosas = lista_cosas

        @Overload
        def sumar(self):
            print('Tienes que darme algo para sumar!')

        @sumar.overload(str)
        def sumar(self, string):
            print(self.nombre + ' ' + string)

        @sumar.overload(int)
        def sumar(self, numero):
            self.edad += numero
            print('{} ahora tiene {} años!'.format(self.nombre, self.edad))

        @sumar.overload(list, tuple)
        def sumar(self, cosas_nuevas, precios):
            self.lista_cosas.extend(cosas_nuevas)
            print('{} ahora tiene todas estas cosas: {} y le costaron ${:,}'.format(self.nombre,
                                                                                    self.lista_cosas,
                                                                                    sum(precios)))

    c = ClaseOverloaded('Juan', 22, ['laptop', 'calculadora'])

    print('Tipado:\n')
    print(suma(1, 2))
    print(sumar_string('Hello', 'World'))
    print(sumar_lista([1, 2, 3], [4, 5, 6], (7, 8, 9)))

    print('\n------\nOverloading:\n')
    c.sumar()
    c.sumar('Solo')
    c.sumar(2)
    c.sumar(['celular', 'chocolate'], (68900, 550))
