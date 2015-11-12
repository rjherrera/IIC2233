# coding=utf-8
import socket
import threading
import os
import sys
import select


class Service:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 10002
        self.historia = []

    def escuchar(self):
        # la idea es recibir la ruta, y si hay empezar a recibir el archivo
        # en caso de q no sea una ruta (no se pueda decodifcar)
        # o que no tenga el patron(caso de q si pueda decodificar pero no es ruta)
        # escribe
        self.ruta = 'aa.txt'
        while True:
            data = self.cliente.recv(1024)
            try:
                posible_ruta = data.decode('utf-8')
                if 'pattern|' in posible_ruta:
                    self.ruta = posible_ruta.split('|')[1]
                else:
                    with open(self.nombre + self.ruta, 'wb+') as f:
                        data = self.cliente.recv(1024)
                        while data:
                            f.write(data)
                            ready = select.select([self.cliente], [], [], 0)
                            if(ready[0]):
                                data = self.cliente.recv(1024)
                            else:
                                data = b''
            except:
                with open(self.nombre + self.ruta, 'wb+') as f:
                    data = self.cliente.recv(1024)
                    while data:
                        f.write(data)
                        ready = select.select([self.cliente], [], [], 0)
                        if(ready[0]):
                            data = self.cliente.recv(1024)
                        else:
                            data = b''

    def enviar(self, ruta):
        with open('Archivos/' + ruta, 'rb+') as file:
            ruta = 'pattern|' + ruta + '|'
            data = file.read()
            nruta = bytearray(ruta, encoding='utf-8')
            self.cliente.send(nruta)
            self.cliente.send(data)


class Cliente(Service):
    def __init__(self):
        super().__init__()
        self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.cliente.connect((self.host, self.port))
        except socket.error as err:
            print(err)
            sys.exit()
        self.nombre = 'Cliente_'


class Servidor(Service):
    def __init__(self):
        super().__init__()
        self.servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.servidor.bind((self.host, self.port))
        self.servidor.listen(1)
        self.cliente = None
        self.nombre = 'Servidor_'

    def aceptar(self):
        cliente, address = self.servidor.accept()
        self.cliente = cliente
        thread = threading.Thread(target=self.escuchar)
        thread.daemon = True
        thread.start()


def menu():
    print('(1)Mostrar por enviar\n(2)Agregar archivos\n' +
          '(3)Quitar archivos\n(4)Enviar archivos\n(5)Terminar comunicacion')
    while True:
        opcion = input('Seleccione su opción: ')
        if opcion in ['1', '2', '3', '4', '5']:
            return int(opcion)
        print('Seleccione una válida.')


def main(usuario):
    por_enviar = []
    while True:
        opcion = menu()
        if opcion == 1:
            print('Lista de archivos por enviar:')
            print(por_enviar)
        elif opcion == 2:
            print('Lista de archivos en su pc:')
            posibles = os.listdir('Archivos')
            print(posibles)
            while True:
                arch = input('Ingrese el archivo a agregar o 0 para terminar:')
                if arch == '0':
                    break
                if arch in posibles:
                    por_enviar.append(arch)
                    print('Archivo %s agregado al envio.' % arch)
        elif opcion == 3:
            print('Lista de archivos por enviar:')
            print(por_enviar)
            while True:
                arch = input('Ingrese el archivo a sacar o 0 para terminar:')
                if arch == '0':
                    break
                if arch in por_enviar:
                    por_enviar.pop(arch)
                    print('Archivo %s eliminado del envio.' % arch)
        elif opcion == 4:
            print('Lista de archivos por enviar:')
            print(por_enviar)
            for arch in por_enviar:
                usuario.enviar(arch)
        elif opcion == 5:
            usuario.cliente.close()
            if hasattr(usuario, 'servidor'):
                usuario.servidor.close()


if __name__ == "__main__":
    tipo = input("Ingrese S si quiere ser servidor o C si desea ser cliente: ")
    if tipo in ['S', 's']:
        server = Servidor()
        server.aceptar()
        while True:
            main(server)

    elif tipo in ['C', 'c']:
        client = Cliente()
        escuchador = threading.Thread(target=client.escuchar)
        escuchador.daemon = True
        escuchador.start()
        while True:
            main(client)
