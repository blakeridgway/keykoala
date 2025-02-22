import tkinter as tk
from gui.login_screen import LoginScreen
from gui.main_screen import MainScreen
from crypto.encryption import EncryptionManager
from utils.storage import StorageManager

class PasswordManager:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("KeyKoala")
        self.root.geometry("600x800")
        
        self.storage_manager = StorageManager()
        self.encryption_manager = None
        self.current_screen = None
        
        self.setup_gui()
        
    def setup_gui(self):
        self.show_login_screen()
        
    def show_login_screen(self):
        if self.current_screen:
            self.current_screen.destroy()
        self.current_screen = LoginScreen(self.root, self.on_login)
        
    def show_main_screen(self):
        if self.current_screen:
            self.current_screen.destroy()
        self.current_screen = MainScreen(
            self.root,
            self.encryption_manager,
            self.storage_manager
        )
    
    def on_login(self, master_password):
        self.encryption_manager = EncryptionManager(
            master_password,
            self.storage_manager.get_salt()
        )
        self.show_main_screen()
        
    def run(self):
        self.root.mainloop()