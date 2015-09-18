# coding=utf-8
from grafo import Grafo


def output_puertos_conexiones(grafo, ruta):
    grafo.alternantes_random()
    print('Escribiendo puertos y conexiones en "%s"' % ruta)
    with open(ruta, 'w') as f:
        for nodo in grafo.puertos:  # puerto in grafo.lista_puertos
            linea = 'PUERTO %s\n' % str(nodo.valor.id)  # puerto.id
            f.write(linea)
        for conexion in grafo.conexiones:
            linea = ('CONEXION %s %s%s\n' %
                     (conexion.origen.id, conexion.destino.id,
                      conexion.tipo))
            f.write(linea)
    print('Resultado escrito en "%s"' % ruta)


def output_ruta_a_bummer(grafo, ruta):
    ruta_minima = grafo.ruta_a_bummer()
    print('Escribiendo ruta a Bummer en "%s"' % ruta)
    with open(ruta, 'w') as f:
        for i in range(len(ruta_minima)):
            if i < len(ruta_minima) - 1:
                origen = ruta_minima[i].id
                destino = ruta_minima[i + 1].id
                f.write('CONEXION %d %d\n' % (origen, destino))
    print('Resultado escrito en "%s"' % ruta)


def output_rutas_doble_sentido(grafo, ruta):
    dobles = grafo.rutas_doble_sentido()
    print('Escribiendo rutas de doble sentido en "%s"' % ruta)
    with open(ruta, 'w') as f:
        for conexion in dobles:
            if len(conexion) == 2:
                f.write('PAR %d %d\n' % (conexion[0].id, conexion[1].id))
            elif len(conexion) > 2:
                linea = 'RUTA %d' % conexion[0].id
                for i in conexion[1:]:
                    linea += ' ' + str(i.id)
                f.write(linea + '\n')
    print('Resultado escrito en "%s"' % ruta)


def output_ciclos(grafo, ruta):
    triangulos = grafo.rutas_triangulares()
    cuadrados = grafo.rutas_cuadradas()
    print('Escribiendo ciclos en "%s"' % ruta)
    with open(ruta, 'w') as f:
        for tri in triangulos:
            f.write('%d %d %d\n' % (tri[0].id, tri[1].id, tri[2].id))
        for c in cuadrados:
            f.write('%d %d %d %d\n' % (c[0].id, c[1].id, c[2].id, c[3].id))
    print('Resultado escrito en "%s"' % ruta)


def output_maximo_flujo(grafo, ruta):
    cap, ruta_maxima = grafo.maximo_flujo(int(len(grafo.conexiones) / 200))
    print('Escribiendo ruta de máxima capacidad en "%s"' % ruta)
    with open(ruta, 'w') as f:
        f.write('CAP %d\n' % cap)
        for i in range(len(ruta_maxima.camino)):
            if i < len(ruta_maxima.camino) - 1:
                origen = ruta_maxima.camino[i].id
                destino = ruta_maxima.camino[i + 1].id
                f.write('%d %d\n' % (origen, destino))
    print('Resultado escrito en "%s"' % ruta)


def output_no_cycle(grafo, ruta):
    print('Escribiendo ruta de máxima capacidad en "%s"' % ruta)
    with open(ruta, 'w') as f:
        f.write('Casi')
        pass
    print('Resultado escrito en "%s"' % ruta)


if __name__ == '__main__':
    from datetime import datetime
    i = datetime.utcnow()
    grafo = Grafo()
    grafo.mapear_red()
    print('MapearLaRed:', datetime.utcnow() - i)

    i = datetime.utcnow()
    print()
    output_puertos_conexiones(grafo=grafo, ruta='red.txt')
    print('OutputMapeo:', datetime.utcnow() - i)

    i = datetime.utcnow()
    print()
    output_ruta_a_bummer(grafo=grafo, ruta='rutaABummer.txt')
    print('rutaABummer:', datetime.utcnow() - i)

    i = datetime.utcnow()
    print()
    output_rutas_doble_sentido(grafo=grafo, ruta='rutasDobleSentido.txt')
    print('DosSentidos:', datetime.utcnow() - i)

    i = datetime.utcnow()
    print()
    output_ciclos(grafo=grafo, ruta='ciclos.txt')
    print('RtsCíclicas:', datetime.utcnow() - i)

    i = datetime.utcnow()
    print()
    output_maximo_flujo(grafo=grafo, ruta='rutaMaxima.txt')
    print('FlujoMáximo:', datetime.utcnow() - i)

    # i = datetime.utcnow()
    # print()
    # triangulos = grafo.rutas_triangulares()
    # print('RTriangulos:', datetime.utcnow() - i)

    # i = datetime.utcnow()
    # print()
    # cuadrados = grafo.rutas_cuadradas()
    # print('RtCuadrados:', datetime.utcnow() - i)

    # i = datetime.utcnow()
    # with open('prueba.txt') as f:
    #     print(sum(int(i.strip().split()[3]) for i in f.readlines()))
    # print(datetime.utcnow() - i)
