# coding=utf-8
import socket
import threading
import os
import sys
from time import sleep


class Service:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 10000
        self.historia = []

    def escuchar(self):
        while True:
            data = self.cliente.recv(1024)
            if data:
                self.turno = True
                if data.decode('ascii') == 'salir':
                    print('El otro perdió')
                    print('Cerrando en 3...')
                    sleep(3)
                    sys.exit()
            historia = data.decode('ascii')
            self.historia = historia.split()
            print('El mensaje hasta ahora es:', ' '.join(self.historia))
            print('Se esperaran 10 segundos')
            sleep(10)
            os.system('clear')
            # historia_nueva = historia.split()

    def enviar(self, mensaje):
        if self.turno:
            if len(mensaje.split()) - len(self.historia) != 3:
                print('Solo puedes mandar 3 palabras')
            else:
                if self.historia != mensaje.split()[:-3]:
                    print('Perdiste')
                    print('Cerrando en 3...')
                    self.cliente.send('salir'.encode('ascii'))
                    sleep(3)
                    sys.exit()
                else:
                    mensaje = mensaje.encode('ascii')
                    self.cliente.send(mensaje)
                    self.turno = False
        else:
            print('No es tu turno')


class Cliente(Service):
    def __init__(self):
        super().__init__()
        self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.turno = False
        try:
            self.cliente.connect((self.host, self.port))
        except socket.error as err:
            print(err)
            sys.exit()


class Servidor(Service):
    def __init__(self):
        super().__init__()
        self.servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.servidor.bind((self.host, self.port))
        self.servidor.listen(1)
        self.cliente = None
        self.turno = True

    def aceptar(self):
        cliente, address = self.servidor.accept()
        self.cliente = cliente
        thread = threading.Thread(target=self.escuchar)
        thread.daemon = True
        thread.start()


if __name__ == "__main__":
    tipo = input("Ingrese S si quiere ser servidor o C si desea ser cliente: ")
    if tipo in ['S', 's']:
        server = Servidor()
        server.aceptar()
        while True:
            mensaje = input('Ingrese la historia con sus nuevas palabras (sin puntuacion): ')
            server.enviar(mensaje)

    elif tipo in ['C', 'c']:
        client = Cliente()
        escuchador = threading.Thread(target=client.escuchar)
        escuchador.daemon = True
        escuchador.start()
        while True:
            mensaje = input('Ingrese la historia con sus nuevas palabras (sin puntuacion): ')
            client.enviar(mensaje)
