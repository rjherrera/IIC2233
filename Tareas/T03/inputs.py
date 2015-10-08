def pedir_entero(texto):
    while True:
        entrada = input(texto)
        try:
            return int(entrada)
        except ValueError:
            print('%r no es un entero válido.' % entrada)


def pedir_tupla(texto):
    while True:
        entrada = input(texto)
        try:
            lista = entrada.replace(' ', '').split(',')
            if len(lista) < 2:
                raise ValueError
            return tuple(int(i) for i in lista)
        except ValueError:
            print('%r no es un par válido.' % entrada)


def pedir_restringido(texto, opciones):
    while True:
        entrada = input(texto)
        if entrada in opciones:
            return entrada
        print('%r no es una de las opciones (%s).' %
              (entrada, '/'.join(opciones)))


if __name__ == '__main__':
    n = pedir_entero('Ingrese el tamaño del tablero: ')
    print(n)
    t = pedir_tupla('Ingrese las coordenadas (Ej: 0,1): ')
    print(t)
    r = pedir_restringido('Ingrese la orientación (H/V): ', ['H', 'V'])
    print(r)
