# gui/user_accounts/Login.py

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import keyring
import time 
import json

class LoginComponent(ctk.CTkToplevel):
    def __init__(self, master=None, callback=None, database=None, signup_callback=None):
        super().__init__(master=master)

        self.service_id = 'SCOUT'
        self.keyring = keyring.get_keyring()

        self.callback = callback
        self.database = database

        self.title("Login")
        self.geometry("300x200")
        self.configure(bg="#000000")
        self.attributes("-topmost", True) 

        self.username_label = ctk.CTkLabel(self, text="Username:")
        self.username_label.pack()

        self.username_entry = ctk.CTkEntry(self)
        self.username_entry.pack()

        self.password_label = ctk.CTkLabel(self, text="Password:")
        self.password_label.pack()

        self.password_entry = ctk.CTkEntry(self, show="*")
        self.password_entry.pack()

        self.login_button = ctk.CTkButton(self, text="Login", command=self.login)
        self.login_button.pack()

        self.signup_callback = signup_callback

        self.signup_label = tk.Label(self, text="Don't have an account? Sign up", fg="blue", cursor="hand2")
        self.signup_label.pack()
        self.signup_label.bind("<Button-1>", self.sign_up)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.bind('<Return>', lambda event: self.login())
        # self.after_idle(self.fetch_credentials)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        user = self.database.get_user(username)
        if user and user[2] == password:
            credentials = {'username': username, 'password': password, 'timestamp': time.time()}
            keyring.set_password(self.service_id, 'last_user', username)
            keyring.set_password(self.service_id, username, json.dumps(credentials))
            self.callback(user[1])
            if self.winfo_exists():
                self.destroy()

        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def on_closing(self):
        if self.winfo_exists():
            self.destroy()


    def sign_up(self, event):
        if self.signup_callback:
            self.signup_callback()
            if self.winfo_exists():
                self.destroy()


    # def fetch_credentials(self):
        stored_username = keyring.get_password(self.service_id, 'last_user')
        if stored_username:
            stored_credentials = keyring.get_password(self.service_id, stored_username)
            if stored_credentials:
                credentials = json.loads(stored_credentials)
                if time.time() - credentials['timestamp'] < 3600:
                    self.username_entry.insert(0, credentials['username'])
                    self.password_entry.insert(0, credentials['password'])
                    self.login()
                else:
                    keyring.delete_password(self.service_id, stored_username)