import re
from PySide6 import QtWidgets
from PySide6 import QtCore as qtc

from .delete_user import DeleteUser   

class SignUpComponent(QtWidgets.QDialog):
    def __init__(self, parent=None, callback=None, database=None):
        super().__init__(parent=parent)
        self.callback = callback
        self.database = database
        self.setWindowTitle("Sign Up")
        self.resize(400, 400) 
        self.setStyleSheet("background-color: #000000; color: white;")
        self.setModal(True)

        self.setup_ui()
        self.closeEvent = self.on_closing

    def on_right_click(self, event):
        '''Handler for right click event on entry widgets.'''
        context_menu = QtWidgets.QMenu(self)
        copy_action = context_menu.addAction("Copy")
        paste_action = context_menu.addAction("Paste")
        action = context_menu.exec(event.globalPos())
        if action == copy_action:
            QtWidgets.QApplication.clipboard().setText(self.sender().selectedText())
        elif action == paste_action:
            self.sender().insert(QtWidgets.QApplication.clipboard().text())

    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)

        self.username_label = QtWidgets.QLabel("Username:")
        layout.addWidget(self.username_label)
        self.username_entry = QtWidgets.QLineEdit()
        self.username_entry.setContextMenuPolicy(qtc.Qt.CustomContextMenu)
        self.username_entry.customContextMenuRequested.connect(self.on_right_click)
        layout.addWidget(self.username_entry)

        self.password_label = QtWidgets.QLabel("Password:")
        layout.addWidget(self.password_label)
        self.password_entry = QtWidgets.QLineEdit()
        self.password_entry.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_entry.setContextMenuPolicy(qtc.Qt.CustomContextMenu)
        self.password_entry.customContextMenuRequested.connect(self.on_right_click)
        layout.addWidget(self.password_entry)

        self.confirm_password_label = QtWidgets.QLabel("Confirm Password:")
        layout.addWidget(self.confirm_password_label)
        self.confirm_password_entry = QtWidgets.QLineEdit()
        self.confirm_password_entry.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirm_password_entry.setContextMenuPolicy(qtc.Qt.CustomContextMenu)
        self.confirm_password_entry.customContextMenuRequested.connect(self.on_right_click)
        layout.addWidget(self.confirm_password_entry)

        self.email_label = QtWidgets.QLabel("Email:")
        layout.addWidget(self.email_label)
        self.email_entry = QtWidgets.QLineEdit()
        self.email_entry.setContextMenuPolicy(qtc.Qt.CustomContextMenu)
        self.email_entry.customContextMenuRequested.connect(self.on_right_click)
        layout.addWidget(self.email_entry)

        self.name_label = QtWidgets.QLabel("Full Name:")
        layout.addWidget(self.name_label)
        self.name_entry = QtWidgets.QLineEdit()
        layout.addWidget(self.name_entry)

        self.dob_label = QtWidgets.QLabel("Date of Birth (dd-mm-yyyy):")
        layout.addWidget(self.dob_label)
        self.dob_entry = QtWidgets.QLineEdit()
        layout.addWidget(self.dob_entry)

        self.signup_button = QtWidgets.QPushButton("Sign Up")
        self.signup_button.clicked.connect(self.sign_up)
        layout.addWidget(self.signup_button)

        self.delete_user_button = QtWidgets.QPushButton("Delete User")
        self.delete_user_button.clicked.connect(self.delete_user)
        layout.addWidget(self.delete_user_button)

    def sign_up(self):
        username = self.username_entry.text()
        password = self.password_entry.text()
        confirm_password = self.confirm_password_entry.text()
        email = self.email_entry.text()
        name = self.name_entry.text()
        dob = self.dob_entry.text()
        
        if not self.is_valid_password(password, confirm_password):
            return
        if not self.is_valid_email(email):
            return
        if not self.is_valid_dob(dob):
            return

        user = self.database.get_user(username)
        if user:
            QtWidgets.QMessageBox.critical(self, "Error", "Username already exists.")
        else:
            self.database.add_user(username, password, email, name, dob)
            self.callback(username)
            self.close()

    def delete_user(self):  
        username_to_delete = self.username_entry.text() 
        deleter = DeleteUser()
        deleter.delete_specific_user(username_to_delete)
        QtWidgets.QMessageBox.information(self, "Success", f"User '{username_to_delete}' has been deleted.")

    def on_closing(self, event):
        reply = QtWidgets.QMessageBox.question(self, 'Quit', 'Do you want to quit?',
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    @staticmethod
    def is_valid_password(password, confirm_password):
        if password != confirm_password:
            QtWidgets.QMessageBox.critical(None, "Error", "Passwords do not match.")
            return False
        return True

    @staticmethod
    def is_valid_email(email):
        regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if not re.search(regex, email):
            QtWidgets.QMessageBox.critical(None, "Error", "Invalid email format.")
            return False
        return True 

    @staticmethod
    def is_valid_dob(dob):
        regex = r'^(0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[0-2])-\d{4}$'
        if not re.search(regex, dob):
            QtWidgets.QMessageBox.critical(None, "Error", "Invalid date of birth format. Please use dd-mm-yyyy")
            return False
        return True