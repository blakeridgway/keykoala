import tkinter as tk
from tkinter import ttk

class LoginScreen(ttk.Frame):
    def __init__(self, parent, login_callback):
        super().__init__(parent, padding="20")
        self.login_callback = login_callback
        self.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.setup_gui()
    
    def setup_gui(self):
        ttk.Label(self, text="Master Password:").grid(row=0, column=0, pady=10)
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.grid(row=0, column=1, pady=10)
        
        ttk.Button(
            self,
            text="Login",
            command=self.handle_login
        ).grid(row=1, column=0, columnspan=2, pady=10)
    
    def handle_login(self):
        master_password = self.password_entry.get()
        self.login_callback(master_password)
