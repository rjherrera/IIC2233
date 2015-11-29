from utils import PORT, HOST
import socket
import threading
import sys


class Cliente:

    def __init__(self, usuario=''):
        self.usuario = usuario
        self.host = HOST
        self.port = PORT
        self.s_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection = True
        self.mensajes = []
        try:
            self.s_cliente.connect((self.host, self.port))
            recibidor = threading.Thread(target=self.recibir_mensajes, args=())
            recibidor.daemon = True
            recibidor.start()
        except socket.error:
            print("Error de conexión")
            sys.exit()

    def recibir_mensajes(self):
        while self.connection:
            data = self.s_cliente.recv(1024)
            mensaje = data.decode('utf-8')
            self.mensajes.append(mensaje)

    def enviar(self, mensaje):
        self.s_cliente.send(mensaje.encode('utf-8'))

    def desconectar(self):
        self.connection = False
        self.s_cliente.close()
