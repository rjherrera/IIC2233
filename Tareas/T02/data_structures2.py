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


class NodoComplejo(Nodo):

    def __init__(self, valor_1, valor_2, padre=None):
        self.valor_1 = valor_1
        self.valor_2 = valor_2
        valor = pseudo_hash(valor_1, valor_2)
        super().__init__(valor, padre)


class ArbolComplejo(Arbol):

    def add(self, valor1, valor2):
        if self.nodo_raiz is None:
            self.nodo_raiz = NodoComplejo(valor1, valor2)
        else:
            temp = self.nodo_raiz
            agregado = False
            while not agregado:
                if pseudo_hash(valor1, valor2) <= temp.valor:
                    if temp.hijo_izquierdo is None:
                        temp.hijo_izquierdo = NodoComplejo(
                            valor1, valor2, temp.valor)
                        agregado = True
                    else:
                        temp = temp.hijo_izquierdo
                else:
                    if temp.hijo_derecho is None:
                        temp.hijo_derecho = NodoComplejo(
                            valor1, valor2, temp.valor)
                        agregado = True
                    else:
                        temp = temp.hijo_derecho
        self.len += 1


if __name__ == '__main__':
    arbol = Arbol()
    arbol.add(4)
    arbol.add(1)
    arbol.add(5)
    arbol.add(3)
    arbol.add(20)

    print(arbol.find(210))

    print(21, 21 in arbol, 20, 20 in arbol)

    print('Largo', len(arbol))

    arbol_complejo = ArbolComplejo()
    arbol_complejo.add(1, 2)

    print(3 in arbol_complejo)

    # print(arbol)
