# src/crypto/encryption.py
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class EncryptionManager:
    def __init__(self, master_password, salt):
        self.fernet = self._create_fernet(master_password, salt)
    
    def _create_fernet(self, master_password, salt):
        """Create a Fernet instance using the master password and salt."""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
        return Fernet(key)
    
    def encrypt(self, data):
        """Encrypt the data."""
        return self.fernet.encrypt(data.encode()).decode()
    
    def decrypt(self, encrypted_data):
        """Decrypt the data."""
        return self.fernet.decrypt(encrypted_data.encode()).decode()
