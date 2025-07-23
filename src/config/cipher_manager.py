# PasswordGenerate/src/config/cipher_manager.py

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64
import os
from typing import Tuple

class CipherManager:
    """
    Gerencia a criptografia e descriptografia de senhas usando Fernet (AES).
    A chave Fernet é derivada de uma senha mestra e um salt usando PBKDF2.
    """

    def __init__(self):
        pass

    def _derive_key(self, master_password: str, salt: bytes) -> bytes:
        """
        Deriva uma chave criptográfica de uma senha mestra e um salt usando PBKDF2.
        """
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,  # Chave de 32 bytes para SHA256 para Fernet
            salt=salt,
            iterations=480000,  # Recomenda-se um alto número de iterações para PBKDF2
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(master_password.encode('utf-8')))
        return key

    def generate_master_key_info(self, master_password: str) -> Tuple[str, str]:
        """
        Gera um salt para a senha mestra e deriva a chave Fernet.
        Retorna o salt (hex) e a chave Fernet (urlsafe_b64encoded).
        """
        salt_bytes = os.urandom(16)  # 16 bytes de salt para a chave mestra
        fernet_key_bytes = self._derive_key(master_password, salt_bytes)
        return salt_bytes.hex(), fernet_key_bytes.decode('utf-8')

    def get_fernet_instance(self, master_password: str, master_salt_hex: str) -> Fernet:
        """
        Recria a instância Fernet a partir da senha mestra e do salt armazenado.
        """
        master_salt_bytes = bytes.fromhex(master_salt_hex)
        fernet_key_bytes = self._derive_key(master_password, master_salt_bytes)
        return Fernet(fernet_key_bytes)

    def encrypt_password(self, fernet_instance: Fernet, plain_password: str) -> str:
        """
        Criptografa uma senha em texto puro usando a instância Fernet fornecida.
        Retorna o token cifrado (string).
        """
        token = fernet_instance.encrypt(plain_password.encode('utf-8'))
        return token.decode('utf-8')

    def decrypt_password(self, fernet_instance: Fernet, encrypted_password_token: str) -> str | None:
        """
        Descriptografa um token de senha cifrado usando a instância Fernet fornecida.
        Retorna a senha em texto puro (string) ou None se o token for inválido.
        """
        try:
            decrypted_bytes = fernet_instance.decrypt(encrypted_password_token.encode('utf-8'))
            return decrypted_bytes.decode('utf-8')
        except InvalidToken:
            print("Erro de descriptografia: Token inválido ou chave incorreta.")
            return None
        except Exception as e:
            print(f"Erro inesperado na descriptografia: {e}")
            return None

