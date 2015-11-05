import socket
import threading
from gato import Gato, sys


class Service:
    def __init__(self, gato):
        self.gato = gato
        self.host = '127.0.0.1'
        self.port = 10002

    def escuchar(self):
        while True:
            if self.gato.revisar_ganador():
                print('Gano el jugador %s' % self.gato.turno)
            print(self.gato)
            pos = self.cliente.recv(1024)
            pos = pos.decode('ascii')
            pos = tuple(int(i) for i in pos.split(','))
            self.gato.editar_posicion(pos)

    def enviar(self, mensaje):
        if self.gato.revisar_ganador():
            print('Gano el jugador %s' % self.gato.turno)
        if mensaje:   # la idea es q si no te toca no ingreses nada
            pos = tuple(int(i) for i in mensaje.split(','))
            self.gato.editar_posicion(pos)
        else:
            print('Debe jugar el otro antes.')
        self.cliente.send(mensaje.encode('ascii'))


class Cliente(Service):
    def __init__(self, gato):
        super().__init__(gato)
        self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.cliente.connect((self.host, self.port))
        except socket.error as err:
            print(err)
            sys.exit()
        # finally:
        #     self.cliente.close()


class Servidor(Service):
    def __init__(self, gato):
        super().__init__(gato)
        self.servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.servidor.bind((self.host, self.port))
        self.servidor.listen(1)
        self.cliente = None

    def aceptar(self):
        cliente, address = self.servidor.accept()
        self.cliente = cliente
        thread = threading.Thread(
            target=self.escuchar)  # , args=(cliente,))
        thread.daemon = True
        thread.start()


if __name__ == "__main__":
    gato = Gato()
    pick = input("Ingrese X si quiere ser servidor o O si desea ser cliente: ")
    if pick == "X":
        server = Servidor(gato)
        server.aceptar()
        while True:
            mensaje = input(
                "Jugador {0} debe ingresar la posicion en que desea jugar: "
                .format(server.gato.turno))
            server.enviar(mensaje)

    elif pick == "O":
        client = Cliente(gato)
        escuchador = threading.Thread(target=client.escuchar)
        escuchador.daemon = True
        escuchador.start()
        while True:
            mensajes = input(
                "Jugador {0} debe ingresar la posicion en que desea jugar: "
                .format(client.gato.turno))
            client.enviar(mensajes)
