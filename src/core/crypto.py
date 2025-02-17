# crypto.py
from cryptography.fernet import Fernet

class KeyEncryptor:
    def __init__(self):
        self.key = Fernet.generate_key()
    
    def encrypt_key(self, private_key: str) -> bytes:
        f = Fernet(self.key)
        return f.encrypt(private_key.encode())
    
    def decrypt_key(self, encrypted_key: bytes) -> str:
        f = Fernet(self.key)
        return f.decrypt(encrypted_key).decode()