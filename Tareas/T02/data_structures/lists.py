# coding=utf-8
class Elemento:

    def __init__(self, valor=None):
        self.valor = valor
        self.siguiente = None

    def __repr__(self):
        return str(self.valor)


class List:

    def __init__(self, *args):
        self.ultimo = None
        self.primero = None
        self.len = 0
        for i in args:
            self.append(i)

    def append(self, valor):
        if not self.primero:
            self.primero = Elemento(valor)
            self.ultimo = self.primero
        else:
            self.ultimo.siguiente = Elemento(valor)
            self.ultimo = self.ultimo.siguiente
        self.len += 1

    def popleft(self):
        elemento = self.primero
        self.primero = elemento.siguiente
        self.len -= 1
        return elemento.valor

    def remove(self, elemento):  # diferente porque retorna nueva lista
        if elemento not in self:
            raise ValueError('Lista.remove(x): x not in Lista')
        for i in range(len(self)):
            if self[i] == elemento:
                return self[:i] + self[i + 1:]

    # def pop(self, index=-1):
    #     length = len(self)
    #     returning = self[index]
    #     if length == 0:
    #         raise IndexError('pop from empty List')
    #     if index == -1:
    #         self[-2].siguiente = None
    #         return returning

    # def __contains__(self, element):
    #     return bool(filter(lambda x: x == element, self))

    def __eq__(self, other):
        return len(self) == sum(map(lambda x: x[0] == x[1], zip(self, other)))

    def __len__(self):
        return self.len

    def __add__(self, other):
        new = List()
        for i in self:
            new.append(i)
        for i in other:
            new.append(i)
        return new

    def __getitem__(self, index):
        if isinstance(index, slice):
            step = 1 if index.step is None else index.step
            stop = len(self) if index.stop is None else index.stop
            if stop < 0:
                stop += len(self)
            start = 0 if index.start is None else index.start
            return List(*(self[i] for i in range(start, stop, step)))
        if not isinstance(index, int):
            raise IndexError('Lista indices must be integers, not %s' %
                             type(index).__name__)
        if index < 0:
            index += len(self)
        if index < 0:
            raise IndexError('List index out of range')
        elemento = self.primero
        for i in range(index):
            if elemento:
                elemento = elemento.siguiente
        if elemento:
            return elemento.valor
        raise IndexError('List index out of range')

    def __repr__(self):
        rep = ''
        elemento_actual = self.primero
        while elemento_actual:
            rep += '%r, ' % (elemento_actual.valor)
            elemento_actual = elemento_actual.siguiente
        return 'List(%s)' % rep[:-2]


if __name__ == '__main__':
    lista = List(0, 1, 2, 3, 4, 5, 6, 7)
    print(4 in lista)
    print(lista)
    lista.append('AAA')
    print(lista)
    lista.popleft()
    print(lista)
    print(lista[5])
    print('len(%r)' % lista, len(lista))
    print(lista[:])
    print(lista[1:3])
    print(lista[-1], 'a')
    # print(lista[1:5:1])
    # print(list(lista)[1:5:1])
    # print(len(Lista()))
    # print(lista.pop())
    print(lista)
    print(lista + lista)
    print(lista.remove(6))
    print(lista.remove('AAA')[:-1])
    # print([1, 2, 3][1])
    # print(lista, lista.ultimo, lista.primero)
    print(List(*reversed(lista)))
    print(List(*map(str, [1, 2, 3])))
    print(List(*lista))

    a, b = List(1, 2)
    print(a, b)

    print(list(i for i in lista))

    # del lista[1]
    lista.append(8)
    print(lista)
