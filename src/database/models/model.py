# PasswordGenerate/src/database/models/model.py

class PasswordEntry:
    """
    Representa o modelo de dados para uma entrada de senha.
    Define a estrutura dos dados para uma senha no sistema (ID, Nome, Senha Cifrada, Salt da Chave Mestra, Data de Criação).
    """
    def __init__(self, id: int = None, name: str = None, encrypted_password: str = None, master_key_salt: str = None, created_at: str = None):
        self.id = id
        self.name = name
        self.encrypted_password = encrypted_password
        self.master_key_salt = master_key_salt     # O salt usado para derivar a chave da senha mestra
        self.created_at = created_at

    def __repr__(self):
        encrypted_preview = self.encrypted_password[:10] + '...' if self.encrypted_password else 'None'
        salt_preview = self.master_key_salt[:10] + '...' if self.master_key_salt else 'None'
        return (f"PasswordEntry(id={self.id}, name='{self.name}', "
                f"encrypted_password='{encrypted_preview}', "
                f"master_key_salt='{salt_preview}', created_at='{self.created_at}')")
