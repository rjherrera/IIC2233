from utils.parser import ApacheLogsParser
from functools import reduce
from itertools import groupby


def largo(secuencia):
    secuencia = map(lambda x: 1, secuencia)
    return reduce(lambda x, y: x + y, secuencia)


class BigAnalizador:

    def __init__(self, logs):
        self.logs = logs

    @property
    def sizes(self):
        return map(lambda x: x.size, self.logs)

    def bytes_transferidos(self):
        print(reduce(lambda x, y: x + y, self.sizes))

    def errores_servidor(self):
        print(largo(filter(lambda x: x.status in [404, 500, 501], self.logs)))

    def solicitudes_exitosas(self):
        print(largo(filter(lambda x: x.status in [200, 302, 304], self.logs)))

    def url_mas_solicitada(self):
        logs = sorted(self.logs, key=lambda x: x.request)
        l = sorted(groupby(logs, lambda x: x.request), key=lambda x: x[1])
        print(l[0][0])

        # print(groupby(self.logs, key=lambda x: x.request))


if __name__ == '__main__':
    parser = ApacheLogsParser("./utils/nasa_logs_week.txt")
    logs = parser.get_apache_logs()
    biganalizador = BigAnalizador(logs)

    biganalizador.bytes_transferidos()
    biganalizador.errores_servidor()
    biganalizador.solicitudes_exitosas()
    biganalizador.url_mas_solicitada()
