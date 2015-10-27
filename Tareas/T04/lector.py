def leer_mapa(ruta):
    casas = []
    calles = []
    vacios = []
    with open(ruta) as f:
        dim = tuple(int(i) for i in f.readline().strip().split('x'))
        dim = dim[0], dim[1] + 1
        for line in (i.strip() for i in f.readlines()):
            if 'calle' in line:
                things = line.split()
                pos = tuple(int(i) + 1 for i in things[0].split(','))
                calles.append({'sentido': things[2], 'posicion': pos})
            elif 'vacio' in line:
                things = line.split()
                pos = tuple(int(i) + 1 for i in things[0].split(','))
                vacios.append({'posicion': pos})
            elif 'casa de' in line:
                line = line.replace('casa de ', '').replace(', ', ',')
                things = line.split()
                pos = tuple(int(i) + 1 for i in things[0].split(','))
                robos = tuple(int(i) for i in things[2][1:-1].split(','))
                dicc = {'posicion': pos, 'rango_robos': robos,
                        'material': things[1]}
                casas.append(dicc)  # pos + (things[1],) + robos)
    return dim, calles, vacios, casas


# def normalizar(calles, casas):
#     for calle in calles:
#         dicc =
#     return dicc_calles, dicc_casas


if __name__ == '__main__':
    print(leer_mapa('mapa fix.txt'))