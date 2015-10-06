import threading


class Worker(threading.Thread):
    mean_data = dict()      # para guardar los promedios
    threads = {}
    # Sientete libre para usar otras
    # variables estaticas aqui si quieres

    # programa el __init__
    # recuerda imprimir cual es el comando
    # para el cual se creo el worker
    def __init__(self, star_name, function_name):
        super().__init__()
        self.daemon = True
        self.function = self.functions(function_name)
        self.star_name = star_name
        self.function_name = function_name

    @property
    def name(self):
        return self.function_name + ' ' + self.star_name

    @staticmethod
    def functions(func_name):
        """
        Este metodo recibe el nombre de una funcion
        y retorna una funcion que calcula promedio
        o varianza segun el argumento.
        Se necesita haber calculado promedio
        para poder calcular varianza
        """

        def mean(star_name):
            with open("{}.txt".format(star_name), 'r') as file:
                lines = file.readlines()
                ans = sum(map(lambda l: float(l), lines))/len(lines)
                Worker.mean_data[star_name] = ans
                return ans

        def var(star_name):
            prom = Worker.mean_data[star_name]
            with open("{}.txt".format(star_name), 'r') as file:
                lines = file.readlines()
                n = len(lines)
                suma = sum(map(lambda l: (float(l) - prom)**2, lines))
                return suma/(n-1)

        return locals()[func_name]

    # escriba el metodo run
    def run(self):
        if self.function_name == 'var':
            if self.star_name not in self.__class__.mean_data:
                print('No se puede porque no se ha calculado la',
                      'mean de %s.' % self.star_name)
            else:
                self.__class__.threads[self.star_name + self.function_name] = self
                res = self.function(self.star_name)
                print('Thread "%s %s" terminado. Var es: %f' %
                      (self.function_name, self.star_name, res))
        elif self.function_name == 'mean':
            print('Calculando mean de %s' % self.star_name)
            self.__class__.threads[self.star_name + self.function_name] = self
            res = self.function(self.star_name)
            print('Thread "%s %s" terminado. Mean es: %f' %
                  (self.function_name, self.star_name, res))


if __name__ == "__main__":
    command = input("Ingrese siguiente comando:\n")

    while command != "exit":
        command = command.split(' ')
        if command[0] == 'mean':
            w = Worker(command[1], command[0])
            if (w.star_name + w.function_name in w.__class__.threads and
                    w.__class__.threads[w.star_name + w.function_name].isAlive()):
                print('El comando ya se está ejecutando por un worker.')
            else:
                print('Se está ejecutando %s' % w.name)
                w.start()
        elif command[0] == 'var':
            w = Worker(command[1], command[0])
            if (w.star_name + w.function_name in w.__class__.threads and
                    w.__class__.threads[w.star_name + w.function_name].isAlive()):
                print('El comando ya se está ejecutando por un worker.')
            else:
                print('Se está ejecutando %s' % w.name)
                w.start()

        # Complete el main:
        #   - Que no se caiga el programa al ingresar inputs invalidos
        #   - Revisar que no haya un worker ejecutando el comando
        #   - Revisar que solo se puede calcular var estrella
        #           si ya se calculo mean estrella
        #   - Si corresponde: crear worker, echarlo a correr

        command = input("Ingrese siguiente comando:\n")
    d = Worker.threads
    for key in d:
        if not d[key].isAlive():
            print('Alcanzó: ' + d[key].name)
        else:
            print('No alcanzó: ' + d[key].name)
