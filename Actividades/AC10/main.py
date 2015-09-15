def __init__(self, *args, **kwargs):
    for i, j in zip(self.attributes, args):  # asumo que lo da en orden
        self.__dict__[i] = j
    del self.__class__.attributes


def __setattr__(obj, attributes, value):
    raise AttributeError('can\'t set attribute')


class RestrictedAccess(type):

    def __new__(cls, nombre, base_clases, diccionario):
        diccionario['__init__'] = __init__
        diccionario['__setattr__'] = __setattr__
        return super().__new__(cls, nombre, base_clases, diccionario)


class Singleton(type):

    def __init__(cls, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cls._unique_instance = None

    def __call__(cls, *args, **kwargs):
        if cls._unique_instance is None:
            cls._unique_instance = super().__call__(*args, **kwargs)
        return cls._unique_instance


if __name__ == '__main__':

    class Person(metaclass=RestrictedAccess):
        attributes = ["name", "lastname", "alias"]

    p = Person("Bruce", "Wayne", "Batman")

    print(p.name, p.lastname, "es", p.alias, "!")
    # # Bruce Wayne es Batman !
    # p.alias = "Robin"
    # # AttributeError : cant set attribute

    class A(metaclass=Singleton):
        def __init__(self, value):
            self.val = value

    a = A(10)
    b = A(20)
    # Se crea una instancia de A
    # Se retorna la instancia que ya estaba creada
    print(a.val, b.val)
    # # 10 10
    print(a is b)
    # # True
