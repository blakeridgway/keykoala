import tkinter as tk
from tkinter import ttk, messagebox
import pyperclip

class MainScreen(ttk.Frame):
    def __init__(self, parent, encryption_manager, storage_manager):
        super().__init__(parent, padding="20")
        self.encryption_manager = encryption_manager
        self.storage_manager = storage_manager
        self.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.setup_gui()
    
    def setup_gui(self):
        self.create_entry_fields()
        self.create_treeview()
        self.create_context_menu()
        self.load_entries()
    
    def create_entry_fields(self):
        ttk.Label(self, text="Site:").grid(row=0, column=0, pady=5)
        self.site_entry = ttk.Entry(self)
        self.site_entry.grid(row=0, column=1, pady=5)
        
        ttk.Label(self, text="Username:").grid(row=1, column=0, pady=5)
        self.username_entry = ttk.Entry(self)
        self.username_entry.grid(row=1, column=1, pady=5)
        
        ttk.Label(self, text="Password:").grid(row=2, column=0, pady=5)
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.grid(row=2, column=1, pady=5)
        
        ttk.Button(
            self,
            text="Add Entry",
            command=self.add_entry
        ).grid(row=3, column=0, columnspan=2, pady=10)
    
    def create_treeview(self):
        columns = ("Site", "Username")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        self.tree.grid(row=4, column=0, columnspan=2, pady=10)
    
    def create_context_menu(self):
        self.popup_menu = tk.Menu(self, tearoff=0)
        self.popup_menu.add_command(
            label="Copy Password",
            command=self.copy_password
        )
        self.popup_menu.add_command(
            label="Delete Entry",
            command=self.delete_entry
        )
        
        self.tree.bind("<Button-3>", self.show_popup_menu)
    
    def show_popup_menu(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.popup_menu.post(event.x_root, event.y_root)
    
    def add_entry(self):
        site = self.site_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not all([site, username, password]):
            messagebox.showerror("Error", "All fields are required!")
            return
        
        encrypted_password = self.encryption_manager.encrypt(password)
        self.storage_manager.add_entry(site, username, encrypted_password)
        self.load_entries()
        self.clear_entries()
    
    def clear_entries(self):
        self.site_entry.delete(0, tk.END)
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
    
    def load_entries(self):
        self.tree.delete(*self.tree.get_children())
        entries = self.storage_manager.get_all_entries()
        
        for site, data in entries.items():
            self.tree.insert("", tk.END, values=(site, data["username"]))
    
    def copy_password(self):
        selected = self.tree.selection()
        if not selected:
            return
        
        site = self.tree.item(selected[0])["values"][0]
        encrypted_password = self.storage_manager.get_password(site)
        decrypted_password = self.encryption_manager.decrypt(encrypted_password)
        pyperclip.copy(decrypted_password)
        messagebox.showinfo("Success", "Password copied to clipboard!")
    
    def delete_entry(self):
        selected = self.tree.selection()
        if not selected:
            return
        
        site = self.tree.item(selected[0])["values"][0]
        self.storage_manager.delete_entry(site)
        self.load_entries()
