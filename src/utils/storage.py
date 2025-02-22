import json
import os
import base64
import secrets

class StorageManager:
    def __init__(self, data_file="passwords.enc"):
        self.data_file = data_file
        self.config_file = "config.json"
        self.passwords = {}
        self.salt = self._get_or_create_salt()
        self._load_data()
    
    def _get_or_create_salt(self):
        """Generate or retrieve the salt from config file."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as f:
                    config = json.load(f)
                    return base64.b64decode(config["salt"])
            except Exception:
                return self._create_new_salt()
        return self._create_new_salt()
    
    def _create_new_salt(self):
        """Generate a new salt and save it to config."""
        salt = secrets.token_bytes(32)  # 32 bytes = 256 bits
        config = {"salt": base64.b64encode(salt).decode()}
        
        with open(self.config_file, "w") as f:
            json.dump(config, f)
        
        return salt
    
    def get_salt(self):
        """Return the current salt."""
        return self.salt    
    
    def _load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}
    
    def _save_data(self):
        with open(self.data_file, "w") as f:
            json.dump(self.passwords, f)
    
    def add_entry(self, site, username, encrypted_password):
        self.passwords[site] = {
            "username": username,
            "password": encrypted_password
        }
        self._save_data()
    
    def get_all_entries(self):
        return self.passwords
    
    def get_password(self, site):
        return self.passwords[site]["password"]
    
    def delete_entry(self, site):
        if site in self.passwords:
            del self.passwords[site]
            self._save_data()
