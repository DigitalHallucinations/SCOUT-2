
import re
import tkinter as tk
from tkinter import messagebox
from .delete_user import DeleteUser   

class SignUpComponent(tk.Toplevel):
    def __init__(self, master=None, callback=None, database=None):
        super().__init__(master=master)
        self.callback = callback
        self.database = database
        self.title("Sign Up")
        self.geometry("400x400")  # Adjusted size for more fields
        self.configure(bg="#000000")
        self.attributes("-topmost", True)

        self.setup_ui()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_right_click(self, event):
        '''Handler for right click event on entry widgets.'''
        context_menu = tk.Menu(self, tearoff=0)
        context_menu.add_command(label="Copy", command=lambda: self.after(10, self.event_generate('<Control-c>')))
        context_menu.add_command(label="Paste", command=lambda: self.after(10, self.event_generate('<Control-v>')))
        context_menu.post(event.x_root, event.y_root)

    def setup_ui(self):

        self.username_label = tk.Label(self, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()
        self.username_entry.bind('<Control-c>', lambda e: self.after(10, self.username_entry.event_generate('<<Copy>>')))
        self.username_entry.bind('<Control-v>', lambda e: self.after(10, self.username_entry.event_generate('<<Paste>>')))
        self.username_entry.bind('<Button-3>', self.on_right_click)

        self.password_label = tk.Label(self, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()
        self.password_entry.bind('<Control-c>', lambda e: self.after(10, self.password_entry.event_generate('<<Copy>>')))
        self.password_entry.bind('<Control-v>', lambda e: self.after(10, self.password_entry.event_generate('<<Paste>>')))
        self.password_entry.bind('<Button-3>', self.on_right_click)

        self.confirm_password_label = tk.Label(self, text="Confirm Password:")
        self.confirm_password_label.pack()
        self.confirm_password_entry = tk.Entry(self, show="*")
        self.confirm_password_entry.pack()
        self.confirm_password_entry.bind('<Control-c>', lambda e: self.after(10, self.confirm_password_entry.event_generate('<<Copy>>')))
        self.confirm_password_entry.bind('<Control-v>', lambda e: self.after(10, self.confirm_password_entry.event_generate('<<Paste>>')))
        self.confirm_password_entry.bind('<Button-3>', self.on_right_click)

        self.email_label = tk.Label(self, text="Email:")
        self.email_label.pack()
        self.email_entry = tk.Entry(self)
        self.email_entry.pack()
        self.email_entry.bind('<Control-c>', lambda e: self.after(10, self.email_entry.event_generate('<<Copy>>')))
        self.email_entry.bind('<Control-v>', lambda e: self.after(10, self.email_entry.event_generate('<<Paste>>')))
        self.email_entry.bind('<Button-3>', self.on_right_click)

        # New fields for name and DOB (to later link with patient chart)
        self.name_label = tk.Label(self, text="Full Name:")
        self.name_label.pack()
        self.name_entry = tk.Entry(self)
        self.name_entry.pack()

        self.dob_label = tk.Label(self, text="Date of Birth (dd-mm-yyyy):")
        self.dob_label.pack()
        self.dob_entry = tk.Entry(self)
        self.dob_entry.pack()

        self.signup_button = tk.Button(self, text="Sign Up", command=self.sign_up)
        self.signup_button.pack()

        self.delete_user_button = tk.Button(self, text="Delete User", command=self.delete_user)
        self.delete_user_button.pack()


    def sign_up(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        email = self.email_entry.get()
        name = self.name_entry.get()
        dob = self.dob_entry.get()
        
        if not self.is_valid_password(password, confirm_password):
            return
        if not self.is_valid_email(email):
            return
        if not self.is_valid_dob(dob):
            return

        user = self.database.get_user(username)
        if user:
            messagebox.showerror("Error", "Username already exists.")
        else:
            # For simplicity, the 'add_user' method now only registers the user.
            # The system will use the provided name and DOB to fetch the patient chart after login.
            self.database.add_user(username, password, email, name, dob)
            self.callback(username)
            self.destroy()

    def delete_user(self):  
        username_to_delete = self.username_entry.get() 
        deleter = DeleteUser()
        deleter.delete_specific_user(username_to_delete)
        messagebox.showinfo("Success", f"User '{username_to_delete}' has been deleted.")

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()

    @staticmethod
    def is_valid_password(password, confirm_password):
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
            return False
        return True

    @staticmethod
    def is_valid_email(email):
        regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if not re.search(regex, email):
            messagebox.showerror("Error", "Invalid email format.")
            return False
        return True 

    @staticmethod
    def is_valid_dob(dob):
        regex = r'^[0-3][0-9]-[0-1][0-9]-[0-9]{4}$'
        if not re.search(regex, dob):
            messagebox.showerror("Error", "Invalid date of birth format. Please use yyyy-mm-dd")
            return False
        return True 