# coding=utf-8


def groups(lista, n):
    j = 0
    for i in range(0, len(lista), n):
        j += 1
        aux = [i + [j] for i in lista[i:i + n]]
        yield aux


with open('bacanosidad.txt', 'r') as f:
    l = [i.strip().strip('\n').replace('\t', '', 2) for i in f.readlines()]
    l = [[j, float(k)] for j, k in [i.split('\t') for i in l]]

l = sorted(l, key=lambda x: -x[1])

cantidad = len(l) // 10

generador = groups(l, cantidad)

bacanosidad_grupo = []
for i in range(10):
    g = next(generador)
    bacanosidad_grupo.extend(g)


if __name__ == '__main__':
    print(bacanosidad_grupo[::200])
