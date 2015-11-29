from utils import PORT, HOST
import socket
import threading
import pickle
import base64
import hashlib
import os


# Para las contraseñas uso hash+salt con salt_per_user
# y múltiples iteraciones para hashear.
class User:

    users = {}

    def __init__(self, username, password):
        self.username = username
        self.__salt, self.__hashed = self.get_hash(password)
        if username not in self.__class__.users:
            self.__class__.users[username] = self

    def get_hash(self, password, salt=None):
        salt = base64.b64encode(os.urandom(32)) if salt is None else salt
        digest = hashlib.sha256(salt + password.encode()).hexdigest()
        for _ in range(0, 100):
            digest = hashlib.sha256(digest.encode()).hexdigest()
        return salt, digest

    def check_password(self, password):
        salt, hashed = self.get_hash(password, self.__salt)
        return hashed == self.__hashed

    @classmethod
    def store_users(cls):
        with open('user_info.dpox', 'wb') as f:
            pickle.dump(cls.users, f)

    @classmethod
    def load_users(cls):
        with open('user_info.dpox', 'rb') as f:
            cls.users.update(pickle.load(f))

    @classmethod
    def login(cls, username, password):
        if username in cls.users:
            user = cls.users[username]
            if user.check_password(password):
                return user
            else:
                return False
        return None

    @classmethod
    def signup(cls, username, password):
        if username in cls.users:
            return False
        return cls(username, password)


class Servidor:

    def __init__(self):
        self.usuario = 'SERVER'
        self.host = HOST
        self.port = PORT
        self.s_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s_servidor.bind((self.host, self.port))
        self.s_servidor.listen(5)
        self.clientes = []
        self.user_clients = {}
        self.connection = True
        thread_aceptar = threading.Thread(target=self.aceptar, args=())
        thread_aceptar.daemon = True
        thread_aceptar.start()

    def aceptar(self):
        while True:
            cliente_nuevo, address = self.s_servidor.accept()
            self.clientes.append(cliente_nuevo)
            thread_mensajes = threading.Thread(target=self.recibir_mensajes,
                                               args=(cliente_nuevo,))
            thread_mensajes.daemon = True
            thread_mensajes.start()

    def recibir_mensajes(self, cliente):
        while self.connection:
            data = cliente.recv(1024)
            mensaje = data.decode('utf-8')
            orden, resto = mensaje.split('|', 1)
            if orden == 'LOGIN':
                user, password = resto.split('|', 1)
                loggeo = User.login(user, password)
                if loggeo:
                    msj = 'SUCCESS|logueado.'
                    self.user_clients[user] = cliente
                elif loggeo is None:
                    user = user[:12] + '...' if len(user) > 13 else user
                    msj = 'ERROR|User %s not found.' % user
                else:
                    msj = 'ERROR|Incorrect password.'
                cliente.send(msj.encode('utf-8'))
            elif orden == 'SIGNUP':
                user, password = resto.split('|', 1)
                signupeo = User.signup(user, password)
                if signupeo:
                    msj = 'SUCCESS|signupeado.'
                else:
                    msj = 'ERROR|Username already taken.'
                cliente.send(msj.encode('utf-8'))
            elif orden == 'GET_HISTORY':
                msj = 'FAIL|'
                cliente.send(msj.encode('utf-8'))
            elif orden == 'CHAT':
                print(resto)
                user, desde, msj = resto.split('|', 2)
                hacia = self.encontrar_cliente(user)
                if hacia:
                    hacia.send(('CHAT|%s|%s' % (desde, msj)).encode('utf-8'))
                    msj = 'SUCCESS|enviado.'
                else:
                    msj = 'ERROR|User not connected.'
                cliente.send(msj.encode('utf-8'))
            elif orden == 'GET_USERS':
                msj = str(list(
                    self.user_clients.keys()))[1:-1].replace(' ', '')
                msj = 'USERS|' + msj
                cliente.send(msj.encode('utf-8'))

            # if mensaje.split(': ')[1] == 'quit':
            #     self.clientes.remove(cliente)

    def enviar(self, mensaje):
        c, mensaje = mensaje.split(',')
        msj_final = self.usuario + ": " + mensaje
        self.clientes[int(c)].send(msj_final.encode('utf-8'))

    def encontrar_cliente(self, username):
        if username in self.user_clients:
            return self.user_clients[username]
        return False

    # def desconectar(self):
    #     for i in self.clientes:
    #         self.enviar()

if __name__ == '__main__':
    try:
        s = Servidor()
        User.load_users()
        while s.connection:
            text = input('Presione cualquier tecla para ver la' +
                         'lista de usuarios actualizada o escriba salir:')
            if text == 'salir':
                # s.desconectar()
                break
            print(list(User.users.keys()))
            print(list(s.clientes))
    finally:
        User.store_users()

    u = User('pepe', 'hola123')
    User.store_users()
