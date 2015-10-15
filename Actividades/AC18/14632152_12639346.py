import random
import simpy

SIM_TIME = 500
INTERVAL = 10
TABLES = 3
NAME = "Cliente {0}"


def paciencia(cliente):
    return 2 * cliente.priority + 7


class Cliente():

    def __init__(self, *args, **kwargs):
        self.priority = kwargs['priority']
        self.name = kwargs['name']
        self.arrive = kwargs['arrive']
        self.number = kwargs['arrival_number']
        self.exit = None


class Restaurante():

    def __init__(self, env, capacity):
        self.env = env
        self.mesas = simpy.PriorityResource(env, capacity=capacity)
        self.__clientes = []
        self.n_atendidos = 1
        self.n_idos_llamada = 0

    @property
    def n_clientes(self):
        return len(self.__clientes)

    def espera(self, cliente):
        """
        ToDo
        """
        with self.mesas.request(priority=cliente.priority) as req:
            # print('[COLA] Ha llegado %s a la cola en tiempo %f' % (cliente.name, self.env.now))
            results = yield req | self.env.timeout(paciencia(cliente))
            self.__clientes.append(cliente)
            if req not in results:
                print('[SALIR] Se fue el %s, el tiempo' % cliente.name,
                      '%f paso antes y se le acabó su paciencia de %d segs.'
                      % (round(self.env.now), paciencia(cliente)))
            else:
                self.n_atendidos += 1
                print('[SENTAR] Se sentó el %s en una mesa en tiempo %d'
                      % (cliente.name, round(self.env.now)))
                if random.randint(0, 9) > 8:
                    self.n_idos_llamada += 1
                    yield self.env.timeout(random.uniform(7, 12))
                    print('[SALIR] Se fue el %s por llamada en tiempo %d.'
                          % (cliente.name, round(self.env.now)))
                else:
                    yield self.env.timeout(random.uniform(30, 40))  # self.env.timeout(round(random.uniform(30, 40)))
                    print('[SALIR] Terminó su almuerzo el %s en tiempo %d'
                          % (cliente.name, round(self.env.now)))


def generador_clientes(env, lambdat, res):
    count = 0
    while True:
        yield env.timeout(random.expovariate(1/lambdat))
        priority = random.randint(0, 25)
        cliente = Cliente(name=NAME.format(count),
                          priority=priority,
                          arrive=int(env.now),
                          arrival_number=count)
        print("[COLA] {0} ha arrivado al restaurant al instante {1} y es el cliente numero {2} del dia con prioridad {3}".format
              (cliente.name, round(env.now), count, priority))
        count += 1
        env.process(res.espera(cliente))


if __name__ == '__main__':
    env = simpy.Environment()
    print('Tenga cuidado de ingresar enteros.')
    mesas = int(input('Ingrese una cantidad de mesas: '))
    intervalo = int(input('Ingrese un intervalo: '))
    limite = int(input('Ingrese un numero entero de tiempo de simulacion: '))
    res = Restaurante(env, mesas)
    print('Se inicia el día con %d mesas disponibles.' % mesas)
    gen = generador_clientes(env, intervalo, res)
    env.process(gen)
    env.run(until=limite)
    print('Se atendieron %d clientes en el día de un total de %d que llegaron.'
          % (res.n_atendidos, res.n_clientes))
    print('Se fueron por llamada %d clientes.' % res.n_idos_llamada)
