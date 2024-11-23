from PySide6 import QtWidgets
from PySide6 import QtCore as qtc
from PySide6 import QtGui as qtg
import keyring
import time 
import json

class LoginComponent(QtWidgets.QDialog):
    def __init__(self, parent=None, callback=None, database=None, signup_callback=None):
        super().__init__(parent=parent)

        self.service_id = 'SCOUT'
        self.keyring = keyring.get_keyring()

        self.callback = callback
        self.database = database

        self.setWindowTitle("Login")
        self.resize(300, 200)
        self.setStyleSheet("background-color: #000000; color: white;")
        self.setModal(True) 

        layout = QtWidgets.QVBoxLayout(self)

        self.username_label = QtWidgets.QLabel("Username:")
        layout.addWidget(self.username_label)

        self.username_entry = QtWidgets.QLineEdit()
        layout.addWidget(self.username_entry)

        self.password_label = QtWidgets.QLabel("Password:")
        layout.addWidget(self.password_label)

        self.password_entry = QtWidgets.QLineEdit()
        self.password_entry.setEchoMode(QtWidgets.QLineEdit.Password)
        layout.addWidget(self.password_entry)

        self.login_button = QtWidgets.QPushButton("Login")
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        self.signup_callback = signup_callback

        self.signup_label = QtWidgets.QLabel("Don't have an account? Sign up")
        self.signup_label.setStyleSheet("color: blue;")
        self.signup_label.setCursor(qtg.QCursor(qtc.Qt.PointingHandCursor))
        self.signup_label.mouseReleaseEvent = self.sign_up
        layout.addWidget(self.signup_label)

        self.closeEvent = self.on_closing

        self.password_entry.returnPressed.connect(self.login)
        qtc.QTimer.singleShot(0, self.fetch_credentials)

    def login(self):
        username = self.username_entry.text()
        password = self.password_entry.text()

        user = self.database.get_user(username)
        if user and user[2] == password:
            credentials = {'username': username, 'password': password, 'timestamp': time.time()}
            keyring.set_password(self.service_id, 'last_user', username)
            keyring.set_password(self.service_id, username, json.dumps(credentials))
            self.callback(user[1])
            self.close()

        else:
            QtWidgets.QMessageBox.critical(self, "Error", "Invalid username or password.")

    def on_closing(self, event):
        event.accept()

    def sign_up(self, event):
        if self.signup_callback:
            self.signup_callback()
            self.close()

    def fetch_credentials(self):
        stored_username = keyring.get_password(self.service_id, 'last_user')
        if stored_username:
            stored_credentials = keyring.get_password(self.service_id, stored_username)
            if stored_credentials:
                credentials = json.loads(stored_credentials)
                if time.time() - credentials['timestamp'] < 3600:
                    self.username_entry.setText(credentials['username'])
                    self.password_entry.setText(credentials['password'])
                    self.login()
                else:
                    keyring.delete_password(self.service_id, stored_username)