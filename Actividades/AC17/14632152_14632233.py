from collections import deque
from random import choice, randrange
from random import expovariate, uniform, randint


"""
Eventos:

Se inicializa el sistema con dos jugadores y uno en la cola desde antes
por lo tanto no "ingresa a la cola" el primero.

Se decide quien gana sumando las probabilidades y escogiendo un aleatorio
entre 1 y esa suma, y si es menor que el primer jugador (su habilidad) gana ese
sino, gana el otro.

1. Llega jugador a la cola
2. Ingresa nuevo jugador a jugar
3. Reingresa el que perdió si se cumple cierta probabilidad


Variables de estado relevantes:
1. Reloj de la simulación (tiempo actual de simulación)
2. Tiempo de partido
3. Tiempo de llegada del prox jugador a la cola
4. Tiempo próxima instancia de cada evento
"""


class Jugador:
    # Esta clase modela los autos que llegan a la revision

    def __init__(self):
        self.tipo_vehiculo = choice(['moto', 'camioneta', 'auto'])
        self.habilidad = uniform(1, 10)
        self.jugados = 0

    def __repr__(self):
        return 'Tipo vehiculo: {0}'.format(self.tipo_vehiculo)


class Mesa:

    def __init__(self):
        self.jugador_a = Jugador()
        self.jugador_b = Jugador()
        self.tiempo_juego = round(uniform(4, 6))
        print('[ENTRA] Comienza el recreo')
        # self.tipos = tipos

    def pasar_jugador(self, jugador):
        # self.tarea_actual = vehiculo
        jugador_ido = self.jugador_b
        self.jugador_b = jugador
        # total = self.jugador_a.habilidad + self.jugador_b.habilidad
        # hab_ganadora = uniform(1, total)
        # self.jugador_a.jugados += 1
        # self.jugador_b.jugados += 1
        # if hab_ganadora <= self.jugador_a.habilidad:
        #     perdedor = self.jugador_b
        #     self.jugador_b = jugador
        # else:
        #     perdedor = self.jugador_a
        #     self.jugador_a = jugador
        # Creamos un tiempo de atención aleatorio
        self.tiempo_juego = round(uniform(4, 6))
        return jugador_ido

    @property
    def ocupado(self):
        return self.jugador_a is not None or self.jugador_b is not None


class Simulacion:
    # Esta clase implemeta la simulación. También se puede usar una función como en el caso anterior.
    # Se inicializarn todas las variables utilizadas en la simulación.

    def __init__(self, tiempo_maximo, tasa_llegada):
        self.tiempo_maximo_sim = tiempo_maximo
        self.tasa_llegada = tasa_llegada
        self.tiempo_simulacion = 0
        self.tiempo_proximo_jugador = round(expovariate(self.tasa_llegada) + 0.5)
        self.tiempo_partido = 0
        self.tiempo_espera = 0
        self.mesa = Mesa()
        self.cola_espera = deque()
        self.cola_espera.append(Jugador())
        self.partidos_jugados = 0

    def proximo_jugador(self):
        self.tiempo_proximo_jugador = self.tiempo_simulacion + \
            round(expovariate(self.tasa_llegada) + 0.5)

    def run(self):
        # Este método ejecuta la simulación de la revisión y la cola de espera
        # se estima aleatoreamente la llegada de un auto a la linea de revisión
        self.proximo_jugador()

        while self.tiempo_simulacion < self.tiempo_maximo_sim:

            if self.tiempo_proximo_jugador <= self.tiempo_partido:
                print('[COLA] Se mete a la cola a la espera de jugar')
                self.cola_espera.append(Jugador())
                self.tiempo_simulacion = self.tiempo_proximo_jugador
                self.proximo_jugador()

            if self.tiempo_partido <= self.tiempo_proximo_jugador:
                total = self.mesa.jugador_a.habilidad + self.mesa.jugador_b.habilidad
                hab_ganadora = uniform(1, total)
                self.mesa.jugador_a.jugados += 1
                self.mesa.jugador_b.jugados += 1
                if hab_ganadora <= self.mesa.jugador_a.habilidad:
                    perdedor = self.mesa.jugador_b
                    ganador = self.mesa.jugador_a
                else:
                    perdedor = self.mesa.jugador_a
                    ganador = self.mesa.jugador_b
                self.mesa.jugador_a = ganador
                self.mesa.jugador_b = perdedor
                self.partidos_jugados += 1
                self.tiempo_espera += self.mesa.tiempo_juego
                if len(self.cola_espera) > 0:
                    print('[ENTRA] Ingresa jugador nuevo a jugar')
                    sale = self.mesa.pasar_jugador(self.cola_espera.popleft())
                    aleatorio = randint(0, sale.jugados ** 5)
                    if aleatorio < sale.jugados ** 4:
                        self.cola_espera.append(sale)
                        print('[COLA] Reingresa el jugador a la cola')
                        # la prob de quedarse es 4/5 ** numero de partidos jugados
                    else:
                        print('[SALE] Un jugador no reingresa a la cola, se va')
                    self.tiempo_simulacion = self.tiempo_partido
                    self.tiempo_partido = self.tiempo_simulacion + self.mesa.tiempo_juego
                else:
                    break

        print()
        print('Estadísticas:')
        print('Tiempo total juego {0} min.'.format(self.tiempo_espera))
        print('Total de partidos jugados: {0}'.format(
            self.partidos_jugados))
        print('Tiempo promedio de espera para jugar{0} min.'.format(
            round(self.tiempo_espera / self.partidos_jugados)))

if __name__ == '__main__':

    tasa_llegada_jugadores = 1 / 15
    s = Simulacion(50, tasa_llegada_jugadores)
    s.run()
