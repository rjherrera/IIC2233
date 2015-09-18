def pseudo_hash(value1, value2):
    return value1 * 100000000 + value2


class Nodo:

    def __init__(self, valor, padre=None):
        self.valor = valor
        self.padre = padre
        self.hijo_izquierdo = None
        self.hijo_derecho = None

    def __iter__(self):
        if self.hijo_izquierdo is not None:
            for i in iter(self.hijo_izquierdo):
                yield i
        yield self
        if self.hijo_derecho is not None:
            for i in iter(self.hijo_derecho):
                yield i


class Arbol:

    def __init__(self, nodo_raiz=None):
        self.nodo_raiz = nodo_raiz
        self.len = 0

    @property
    def raiz(self):
        return self.nodo_raiz.valor

    def add(self, valor):
        if self.nodo_raiz is None:
            self.nodo_raiz = Nodo(valor)
        else:
            temp = self.nodo_raiz
            agregado = False
            while not agregado:
                if valor <= temp.valor:
                    if temp.hijo_izquierdo is None:
                        temp.hijo_izquierdo = Nodo(valor, temp.valor)
                        agregado = True
                    else:
                        temp = temp.hijo_izquierdo
                else:
                    if temp.hijo_derecho is None:
                        temp.hijo_derecho = Nodo(valor, temp.valor)
                        agregado = True
                    else:
                        temp = temp.hijo_derecho
        self.len += 1

    def find(self, valor):
        temp = self.nodo_raiz
        while temp:
            if valor == temp.valor:
                return temp.valor
            elif valor < temp.valor:
                temp = temp.hijo_izquierdo
            else:
                temp = temp.hijo_derecho
        return None

    def __iter__(self):
        return iter(self.nodo_raiz)

    def __len__(self):
        return self.len

    def __contains__(self, valor):
        temp = self.nodo_raiz
        while temp:
            if valor == temp.valor:
                return True
            elif valor < temp.valor:
                temp = temp.hijo_izquierdo
            else:
                temp = temp.hijo_derecho
        return False

    def __getitem__(self, index):  # obtiene el i-ésimo valor, pero ordenado
        if not isinstance(index, int):
            raise IndexError('Arbol indices must be integers, not %s' %
                             type(index).__name__)
        if index < 0:
            index += len(self)
        iterator = iter(self)
        if not 0 <= index < len(self):
            raise IndexError('Arbol index out of range')
        for i in range(index):
            next(iterator)
        return next(iterator).valor


if __name__ == '__main__':
    arbol = Arbol()
    arbol.add(4)
    arbol.add(1)
    arbol.add(5)
    arbol.add(3)
    arbol.add(20)

    print('Raiz:', arbol.raiz)
    print('Index -2:', arbol[-2])
    print('Index 4:', arbol[4])

    print('Find 21:', arbol.find(21))
    print('Find 20:', arbol.find(20))

    print('21 in arbol:', 21 in arbol)
    print('20 in arbol:', 20 in arbol)

    print('Largo:', len(arbol))
    print('Phash(1100, 1000):', pseudo_hash(1122, 1035))
