import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import re

from Domain.user_validator import UserValidator
from Repository.repository_json import RepositoryJson
from Service.user_service import UserService


class LoginRegisterPage(tk.Tk):
    user_repository_json = RepositoryJson("Resources/users.json")
    user_validator = UserValidator()
    user_service = UserService(user_repository_json, user_validator)

    def get_credentials(self):
        return self.credentials

    def set_credentials(self, credentials):
        self.credentials = credentials

    def __init__(self):
        super().__init__()
        self.credentials = None

        self.title("Login/Register")
        self.geometry('400x250')

        self.login_frame = ttk.Frame(self)
        self.login_frame.pack(padx=40, pady=20)

        self.username_label = ttk.Label(self.login_frame, text="Username or Email")
        self.username_label.grid(row=0, column=0, sticky="w")

        self.username_entry = ttk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1)

        self.password_label = ttk.Label(self.login_frame, text="Password")
        self.password_label.grid(row=1, column=0, sticky="w")

        self.password_entry = ttk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1)

        self.login_button = ttk.Button(self.login_frame, text="Login", command=self.login)
        self.login_button.grid(row=2, column=0, pady=10)

        self.register_login_button = ttk.Button(self.login_frame, text="Register", command=self.show_register)
        self.register_login_button.grid(row=2, column=1, pady=10)

        self.register_frame = ttk.Frame(self)
        self.register_frame.pack(padx=20, pady=20)

        self.new_username_label = ttk.Label(self.register_frame, text="New Username")
        self.new_username_label.grid(row=0, column=0, sticky="w")

        self.new_username_entry = ttk.Entry(self.register_frame)
        self.new_username_entry.grid(row=0, column=1)

        self.new_email_label = ttk.Label(self.register_frame, text="New Email")
        self.new_email_label.grid(row=1, column=0, sticky="w")

        self.new_email_entry = ttk.Entry(self.register_frame)
        self.new_email_entry.grid(row=1, column=1)

        self.new_password_label = ttk.Label(self.register_frame, text="New Password")
        self.new_password_label.grid(row=2, column=0, sticky="w")

        self.new_password_entry = ttk.Entry(self.register_frame, show="*")
        self.new_password_entry.grid(row=2, column=1)

        self.confirm_password_label = ttk.Label(self.register_frame, text="Confirm Password")
        self.confirm_password_label.grid(row=3, column=0, sticky="w")

        self.confirm_password_entry = ttk.Entry(self.register_frame, show="*")
        self.confirm_password_entry.grid(row=3, column=1)

        self.register_button = ttk.Button(self.register_frame, text="Register", command=self.register)
        self.register_button.grid(row=4, column=0, pady=10)

        self.back_button = ttk.Button(self.register_frame, text="Back", command=self.back)
        self.back_button.grid(row=4, column=1, pady=10)

        self.show_login()

    def show_login(self):
        self.login_frame.pack(padx=40, pady=20)
        self.register_frame.pack_forget()

    def show_register(self):
        self.login_frame.pack_forget()
        self.register_frame.pack(padx=40, pady=20)

    def back(self):
        self.register_frame.pack_forget()
        self.login_frame.pack(padx=40, pady=20)

    def login(self):
        username_or_email = self.username_entry.get()
        password = self.password_entry.get()

        if not username_or_email or not password:
            self.clear_login_labels()
            if not username_or_email:
                self.username_label_error = ttk.Label(self.login_frame, text="Please enter a username or email")
                self.username_label_error.grid(row=3, column=1)
            if not password:
                self.password_label_error = ttk.Label(self.login_frame, text="Please enter a password")
                self.password_label_error.grid(row=4, column=1)
            return

        # Login with email
        if self.email_exists(username_or_email):
            if self.check_password(username_or_email, password):
                tk.messagebox.showinfo("Login successful", f"Welcome {username_or_email}!")
                self.destroy()
                self.credentials = username_or_email
                return
            else:
                self.clear_login_labels()
                self.password_label_error = tk.Label(self.login_frame, text="Incorrect password", fg="red")
                self.password_label_error.grid(row=4, column=1)
            # Login with username
        elif self.username_exists(username_or_email):
            if self.check_password(username_or_email, password):
                tk.messagebox.showinfo("Login successful", f"Welcome {username_or_email}!")
                self.destroy()
                self.credentials = username_or_email
                return
            else:
                self.clear_login_labels()
                self.password_label_error = tk.Label(self.login_frame, text="Incorrect password", fg="red")
                self.password_label_error.grid(row=4, column=1)
        else:
            self.clear_login_labels()
            self.username_label_error = tk.Label(self.login_frame, text="Username or email not found", fg="red")
            self.username_label_error.grid(row=3, column=1)

    def register(self):
        username = self.new_username_entry.get()
        email = self.new_email_entry.get()
        password = self.new_password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if not username or not email or not password or not confirm_password:
            self.clear_register_labels()
            if not username:
                self.new_username_label_error = tk.Label(self.register_frame, text="Please enter a username", fg="red")
                self.new_username_label_error.grid(row=5, column=1)
            if not email:
                self.new_email_label_error = tk.Label(self.register_frame, text="Please enter an email", fg="red")
                self.new_email_label_error.grid(row=6, column=1)
            if not password:
                self.new_password_label_error = tk.Label(self.register_frame, text="Please enter a password", fg="red")
                self.new_password_label_error.grid(row=7, column=1)
            if not confirm_password:
                self.confirm_password_label_error = tk.Label(self.register_frame, text="Please confirm the password",
                                                             fg="red")
                self.confirm_password_label_error.grid(row=8, column=1)
            return

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            self.clear_register_labels()
            self.new_email_label_error = tk.Label(self.register_frame, text="Invalid email format", fg="red")
            self.new_email_label_error.grid(row=6, column=1)
            return

        if self.username_exists(username):
            if self.user_service.get_by_username(username) is not None:
                self.clear_register_labels()
                self.new_username_label_error = tk.Label(self.register_frame, text="Username already taken", fg="red")
                self.new_username_label_error.grid(row=5, column=1)
            return

        if self.email_exists(email):
            if self.user_service.get_by_email(email) is not None:
                self.clear_register_labels()
                self.new_email_label_error = tk.Label(self.register_frame, text="Email already registered", fg="red")
                self.new_email_label_error.grid(row=6, column=1)
            return

        if password != confirm_password:
            self.clear_register_labels()
            self.confirm_password_label_error = tk.Label(self.register_frame, text="Passwords do not match", fg="red")
            self.confirm_password_label_error.grid(row=8, column=1)
            return

        self.user_service.adauga(username, email, password)
        self.clear_register_fields()
        tk.messagebox.showinfo("Registration successful", "You can now log in with your new account")

    def clear_login_labels(self):
        if hasattr(self, "username_label_error"):
            self.username_label_error.destroy()
        if hasattr(self, "password_label_error"):
            self.password_label_error.destroy()

    def clear_register_labels(self):
        if hasattr(self, "new_username_label_error"):
            self.new_username_label_error.destroy()
        if hasattr(self, "new_email_label_error"):
            self.new_email_label_error.destroy()
        if hasattr(self, "new_password_label_error"):
            self.new_password_label_error.destroy()
        if hasattr(self, "confirm_password_label_error"):
            self.confirm_password_label_error.destroy()
        self.new_username_entry.config({"background": "white"})
        self.new_email_entry.config({"background": "white"})
        self.new_password_entry.config({"background": "white"})
        self.confirm_password_entry.config({"background": "white"})

    def clear_register_fields(self):
        self.new_username_entry.delete(0, tk.END)
        self.new_email_entry.delete(0, tk.END)
        self.new_password_entry.delete(0, tk.END)
        self.confirm_password_entry.delete(0, tk.END)

    def username_exists(self, username_or_email):
        for user in self.user_service.get_all():
            if user.username == username_or_email or user.email == username_or_email:
                return True
        return False

    def email_exists(self, email):
        for user in self.user_service.get_all():
            if user.email == email:
                return True
        return False

    def check_password(self, username_or_email, password):
        for user in self.user_service.get_all():
            if user.username == username_or_email or user.email == username_or_email:
                return user.password == password
        return False

    def add_user(self, username, email, password):
        self.user_service.adauga(username, email, password)
