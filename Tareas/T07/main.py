import pickle
from widgets import *
from os import listdir
from PyQt4 import QtGui
from dropbox import Dropbox


class DropBox(QtGui.QMainWindow):

    def __init__(self):
        super().__init__()
        self.central_widget = QtGui.QStackedWidget()
        self.setCentralWidget(self.central_widget)
        self.setWindowTitle('DB PY-IIC')
        self.resize(700, 550)
        self.move(300, 100)
        # Options Widget
        self.widgetOptions = widgetOptions()
        self.central_widget.addWidget(self.widgetOptions)
        # Login Widget
        self.widgetLogin = widgetLogin()
        self.widgetLogin.pushButton.clicked.connect(self.authenticate)
        self.central_widget.addWidget(self.widgetLogin)

        # Verifies if user has the autorization
        if 'db.token' not in listdir():
            self.widgetOptions.hide()
            self.widgetLogin.show()
        else:
            if self.load_token():
                self.widgetLogin.hide()
                self.widgetOptions.show()
                self.widgetOptions.dbx = self.dbx
                self.widgetOptions.thread.start()
            else:
                self.widgetLogin.show()
                self.widgetOptions.hide()

    def authenticate(self):
        auth_code = self.widgetLogin.lineEdit.text()
        try:
            access_token, user_id = self.widgetLogin.auth_flow.finish(
                auth_code)
            self.dbx = Dropbox(access_token)
            user_info = self.dbx.users_get_current_account()
            self.widgetOptions.labelName.setText(user_info.name.display_name)
            self.widgetLogin.hide()
            self.widgetOptions.show()
            self.widgetOptions.dbx = self.dbx
            self.widgetOptions.thread.start()
            self.save_token(access_token)
        except:
            self.widgetLogin.labelError.setText('Invalid code, try again.')

    def save_token(self, token):
        with open('db.token', 'wb') as file:
            pickle.dump(token, file)

    def load_token(self):
        with open('db.token', 'rb') as file:
            try:
                access_token = pickle.load(file)
                self.dbx = Dropbox(access_token)
                user_info = self.dbx.users_get_current_account()
                self.widgetOptions.labelName.setText(
                    user_info.name.display_name)
                return True
            except:
                return False


if __name__ == '__main__':
    app = QtGui.QApplication([])
    form = DropBox()
    form.show()
    app.exec_()
