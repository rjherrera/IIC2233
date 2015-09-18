from functools import reduce


class Arista:

    def __init__(self, elemento, peso):
        self.elemento = elemento
        self.peso = peso

    def __str__(self):
        return str(self.elemento) + str(self.peso)


class Grafo:

    def __init__(self):
        self.relaciones = {}

    def __str__(self):
        return str(self.relaciones)

    def agregar(self, elemento):
        self.relaciones.update({elemento: []})

    def relacionar(self, origen, destino, peso=1):
        self.relaciones[origen].append(Arista(destino, peso))

    def caminoMinimo(self, origen, destino):
        etiquetas = {origen: (0, None)}
        self.dijkstra(destino, etiquetas, [])
        return self.construirCamino(etiquetas, origen, destino)

    def construirCamino(self, etiquetas, origen, destino):
        if origen == destino:
            return [origen]
        return self.construirCamino(etiquetas, origen, anterior(etiquetas[destino])) + [destino]

    def dijkstra(self, destino, etiquetas, procesados):
        nodoActual = menorValorNoProcesado(etiquetas, procesados)
        if (nodoActual == destino):
            return
        procesados.append(nodoActual)
        for vecino in self.vecinoNoProcesado(nodoActual, procesados):
            self.generarEtiqueta(vecino, nodoActual, etiquetas)
        self.dijkstra(destino, etiquetas, procesados)

    def generarEtiqueta(self, nodo, anterior, etiquetas):
        etiquetaNodoAnterior = etiquetas[anterior]
        etiquetaPropuesta = self.peso(anterior, nodo) + acumulado(etiquetaNodoAnterior), anterior
        if (nodo not in etiquetas or
                acumulado(etiquetaPropuesta) < acumulado(etiquetas[nodo])):
            etiquetas.update({nodo: etiquetaPropuesta})

    def aristas(self, nodo):
        return self.relaciones[nodo]

    def vecinoNoProcesado(self, nodo, procesados):
        aristasDeVecinosNoProcesados = filter(
            lambda x: x not in procesados, self.aristas(nodo))
        return [arista.elemento for arista in aristasDeVecinosNoProcesados]

    def peso(self, nodoOrigen, nodoDestino):
        return reduce(
            lambda x, y: x if x.elemento == nodoDestino else y, self.relaciones[nodoOrigen]
        ).peso


def acumulado(etiqueta):
    return etiqueta[0]


def anterior(etiqueta):
    return etiqueta[1]


def menorValorNoProcesado(etiquetas, procesados):
    etiquetadosSinProcesar = filter(lambda nodo: nodo[0] not in procesados, etiquetas.items())
    return min(etiquetadosSinProcesar, key=lambda x: x[1][0])[0]


if __name__ == '__main__':
    buenosAires = "BuenosAires"
    sanPedro = "San Pedro"
    rosario = "Rosario"
    cordoba = "Cordoba"
    villaMaria = "Villa Maria"
    sanLuis = "San Luis"
    mendoza = "Mendoza"
    bahiaBlanca = "Bahia Blanca"

    grafo = Grafo()
    grafo.agregar(buenosAires)
    grafo.agregar(sanLuis)
    grafo.agregar(sanPedro)
    grafo.agregar(rosario)
    grafo.agregar(cordoba)
    grafo.agregar(villaMaria)
    grafo.agregar(bahiaBlanca)
    grafo.agregar(mendoza)

    grafo.relacionar(buenosAires, sanPedro, 175)
    grafo.relacionar(buenosAires, sanLuis, 790)
    grafo.relacionar(buenosAires, bahiaBlanca, 660)

    grafo.relacionar(sanLuis, mendoza, 260)
    grafo.relacionar(sanLuis, villaMaria, 350)
    grafo.relacionar(sanLuis, bahiaBlanca, 800)
    grafo.relacionar(villaMaria, cordoba, 150)
    grafo.relacionar(villaMaria, rosario, 245)
    grafo.relacionar(rosario, sanPedro, 160)

    print(grafo.caminoMinimo(buenosAires, villaMaria))
