# coding=utf-8


class Cancion:

    def __init__(self, nombre):
        self.nombre = nombre


# class Reproductor:

#     def __init__(self, dist_audifono):
#         self.dist_audifono = dist_audifono


class Audifono:

    def __init__(self, frec_min, frec_max, impedancia, int_max):
        self.frec_min = frec_min
        self.frec_max = frec_max
        self.impedancia = impedancia
        self.intensidad_max = int_max

    def escuchar(self, cancion):
        print('La canción %s esta siendo reproducida desde un audífono' %
              cancion.nombre)


class Circumaural(Audifono):

    def __init__(self, aislacion, **kwargs):
        super().__init__(**kwargs)
        self.aislacion = aislacion


class Intraaural(Audifono):

    def __init__(self, incomodidad, **kwargs):
        super().__init__(**kwargs)
        self.incomodidad = incomodidad


class Inalambrico(Audifono):

    def __init__(self, rango, **kwargs):
        super().__init__(**kwargs)
        self.rango = rango
        self.conectado = False

    def conectar(self, dist_audifono):
        if dist_audifono <= self.rango:
            self.conectado = True
            print('Conectado')
        else:
            print('Fuera de rango')

    def escuchar(self, cancion):
        if self.conectado:
            print('La canción %s está siendo reproducida' % cancion.nombre,
                  'desde un audífono inalámbrico')
        else:
            print('No existe conexión, no se reproduce nada')


class Bluetooth(Inalambrico):

    def __init__(self, identificador, **kwargs):
        super().__init__(**kwargs)
        self.identificador = identificador

    def escuchar(self, cancion):
        if self.conectado:
            print('La canción %s está siendo reproducida' % cancion.nombre,
                  'desde un audífono con Bluetooth')
        else:
            print('No existe conexión, no se reproduce nada')


# reproductor = Reproductor(dist_audifono=90)

if __name__ == '__main__':
    from random import randint, uniform

    print('Executing from main\n')

    aud = Audifono(frec_min=randint(20, 100),
                   frec_max=randint(17000, 20000),
                   impedancia=uniform(10, 80),
                   int_max=randint(20, 40))
    crl = Circumaural(aislacion=uniform(0, 100),
                      frec_min=randint(20, 100),
                      frec_max=randint(17000, 20000),
                      impedancia=uniform(10, 80),
                      int_max=randint(20, 40))
    inr = Intraaural(incomodidad=uniform(0, 100),
                     frec_min=randint(20, 100),
                     frec_max=randint(17000, 20000),
                     impedancia=uniform(10, 80),
                     int_max=randint(20, 40))
    inl = Inalambrico(rango=randint(10, 30),
                      frec_min=randint(20, 100),
                      frec_max=randint(17000, 20000),
                      impedancia=uniform(10, 80),
                      int_max=randint(20, 40))
    bth = Bluetooth(identificador='BT-010101',
                    rango=randint(10, 30),
                    frec_min=randint(20, 100),
                    frec_max=randint(17000, 20000),
                    impedancia=uniform(10, 80),
                    int_max=randint(20, 40))

    cancion = Cancion(nombre='Midnight - Coldplay')

    print('Estándar')
    aud.escuchar(cancion)
    print('\nCircumaural')
    crl.escuchar(cancion)
    print('\nIntraaural')
    inr.escuchar(cancion)
    print('\nInalámbrico')
    inl.conectar(dist_audifono=15)
    inl.escuchar(cancion)
    print('\nBluetooth:')
    bth.conectar(dist_audifono=20)
    bth.escuchar(cancion)
