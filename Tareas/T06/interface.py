from PyQt4 import uic, QtCore, QtGui
from cliente import Cliente
from utils import EMOJIS

form = uic.loadUiType("drobpox.ui")


class MainWindow(form[0], form[1]):

    def __init__(self, app):
        super().__init__()
        self.cliente = Cliente()
        self.app = app
        self.setupUi(self)

        self.chatWidget.hide()

        # INPUTS
        # Passwords (enable masking)
        self.lineEditPassword.setEchoMode(QtGui.QLineEdit.Password)
        self.lineEditNewPassword.setEchoMode(QtGui.QLineEdit.Password)
        self.lineEditNewPasswordCheck.setEchoMode(QtGui.QLineEdit.Password)
        # Max_Length callback
        self.lineEditNewUsername.textChanged.connect(
            self.length_check_callback)
        # Match_passwords callback
        self.lineEditNewPasswordCheck.textChanged.connect(
            self.pass_check_callback)
        # INPUTS

        # LOGIN / SIGNUP
        self.pushButtonSignup.clicked.connect(self.signup)
        self.pushButtonLogin.clicked.connect(self.login)
        # LOGIN / SIGNUP

        # OTROS
        self.textBrowserChat.setAcceptRichText(True)
        self.comboBoxChat.currentIndexChanged.connect(self.chat_history)
        self.pushButtonChat.clicked.connect(self.send_message)
        self.chat_timer = QtCore.QTimer(interval=10,
                                        timeout=self.recieve_message)
        self.get_users_timer = QtCore.QTimer(interval=1,
                                             timeout=self.get_users)
        self.plainTextEditChat.textChanged.connect(
            self.msj_length_check_callback)

        self.loginWidget.show()

    def length_check_callback(self):
        sender = self.sender()
        text = sender.text()
        if len(text) > 15:
            sender.setText(text[:15])
            self.labelRegError.setText('Username length must not exceed 15.')
        else:
            self.labelRegError.setText('')

    def msj_length_check_callback(self):
        text = self.sender().toPlainText()
        if len(text) > 900:
            self.sender().setPlainText(text[:900])
            self.labelChatError.setText('Message length must not exceed 900.')
        else:
            self.labelChatError.setText('')

    def pass_check_callback(self):
        pass_check = self.lineEditNewPasswordCheck.text()
        password = self.lineEditNewPassword.text()
        if password != pass_check and len(pass_check) >= len(password):
            self.labelRegError.setText('Passwords don\'t match.')
        elif len(password) < 6:
            self.labelRegError.setText(
                'Password must be at least 6\n characters long.')
        else:
            self.labelRegError.setText('')

    def get_users(self):
        self.cliente.enviar('GET_USERS|')
        self.get_users_timer.setInterval(10000)
        while not self.cliente.mensajes:
            pass
        respuesta, resto = self.cliente.mensajes.pop().split('|', 1)
        print(respuesta)
        usuarios = resto.split(',')
        self.comboBoxChat.addItems(usuarios)

    def chat_history(self):
        user = self.comboBoxChat.itemText(self.comboBoxChat.currentIndex())
        self.cliente.enviar('GET_HISTORY|%s' % user)
        while not self.cliente.mensajes:
            pass
        respuesta, resto = self.cliente.mensajes.pop().split('|', 1)
        if respuesta == 'SUCCESS':
            self.textBrowserChat.setText(resto)

    def send_message(self):
        msj = self.plainTextEditChat.toPlainText()
        msj = msj.replace(':)', EMOJIS[':)']).replace(':(', EMOJIS[':('])
        to = self.comboBoxChat.itemText(self.comboBoxChat.currentIndex())
        self.cliente.enviar('CHAT|%s|%s|%s' % (to, self.cliente.username, msj))
        while not self.cliente.mensajes:
            pass
        respuesta, resto = self.cliente.mensajes.pop().split('|', 1)
        if respuesta == 'SUCCESS':
            print('resto')

    def recieve_message(self):
        mensaje = self.cliente.mensajes[-1]
        if 'CHAT' in mensaje:
            respuesta, resto = self.cliente.mensaje.pop().split('|', 1)
            mensaje = resto.replace('|', ': ', 1)
            self.textBrowserChat.setHtml(mensaje)

    def signup(self):
        username = self.lineEditNewUsername.text()
        password = self.lineEditNewPassword.text()
        pass_check = self.lineEditNewPasswordCheck.text()
        if not username or len(username) < 4:
            self.labelRegError.setText(
                'Username must be at least 4\n characters long.')
            return
        if len(password) < 6:
            self.labelRegError.setText(
                'Password must be at least 6\n characters long.')
            return
        elif pass_check != password:
            self.labelRegError.setText('Passwords don\'t match.')
            return
        self.cliente.enviar(
            'SIGNUP|%s|%s' % (username, password))
        while not self.cliente.mensajes:
            # se espera la respuesta del servidor
            pass
        respuesta, resto = self.cliente.mensajes.pop().split('|', 1)
        if respuesta == 'SUCCESS':
            print(resto)
            self.loginWidget.hide()
            self.chatWidget.show()
            self.labelRegError.setText('')
        elif respuesta == 'ERROR':
            self.labelRegError.setText(resto)

    def login(self):
        self.cliente.enviar(
            'LOGIN|%s|%s' % (self.lineEditUsername.text(),
                             self.lineEditPassword.text()))
        while not self.cliente.mensajes:
            # se espera la respuesta del servidor
            pass
        respuesta, resto = self.cliente.mensajes.pop().split('|', 1)
        if respuesta == 'SUCCESS':
            print(resto)
            self.loginWidget.hide()
            self.chatWidget.show()
            self.labelLogError.setText('')
            self.cliente.username = self.lineEditUsername.text()
        elif respuesta == 'ERROR':
            self.labelLogError.setText(resto)


if __name__ == '__main__':
    app = QtGui.QApplication([])
    form = MainWindow(app)
    form.show()
    app.exec_()
