# PythonPasswordGenerate/src/database/services/security_service.py

import hashlib
import os
from typing import Tuple, List, Dict, Optional

from src.database.repositories.repository import PasswordRepository
from src.database.repositories.repository_config import ConfigRepository
from src.database.models.model import PasswordEntry
from src.config.cipher_manager import CipherManager

MASTER_SALT_SETTING_KEY = "master_password_salt"

class SecurityService:
    """
    Fornece serviços relacionados à segurança de senhas, como gerenciamento
    da senha mestra, criptografia/descriptografia e persistência.
    """

    def __init__(self, password_repository: PasswordRepository, config_repository: ConfigRepository,
                 cipher_manager: CipherManager = None):
        self.repo = password_repository
        self.config_repo = config_repository
        self.cipher_manager = cipher_manager if cipher_manager else CipherManager()
        self._current_fernet_instance = None  # Armazena a instância Fernet após login
        print("DEBUG SecurityService: Instância de SecurityService criada.")

    def is_master_password_set(self) -> bool:
        """
        Verifica se a senha mestra já foi configurada (se o salt existe no DB de configurações).
        """
        is_set = self.config_repo.get_setting(MASTER_SALT_SETTING_KEY) is not None
        print(f"DEBUG SecurityService: is_master_password_set() retornou: {is_set}")
        return is_set

    def register_master_password(self, master_password: str) -> bool:
        print("DEBUG SecurityService: Tentando registrar senha mestra.")
        if self.is_master_password_set():
            print("DEBUG SecurityService: Senha mestra já configurada, não pode registrar novamente.")
            return False

        master_salt_hex, _ = self.cipher_manager.generate_master_key_info(master_password)

        if self.config_repo.set_setting(MASTER_SALT_SETTING_KEY, master_salt_hex):
            print(f"DEBUG SecurityService: Salt da senha mestra '{master_salt_hex}' salvo no DB de configurações.")
            return True
        else:
            print("DEBUG SecurityService: Falha ao salvar salt da senha mestra no DB de configurações.")
            return False

    def login_with_master_password(self, master_password: str) -> bool:
        print("DEBUG SecurityService: Tentando login com senha mestra.")
        stored_master_salt_hex = self.config_repo.get_setting(MASTER_SALT_SETTING_KEY)
        print(f"DEBUG SecurityService: Salt da senha mestra recuperado do DB: {stored_master_salt_hex}")

        if not stored_master_salt_hex:
            print("DEBUG SecurityService: Salt da senha mestra NÃO encontrado no DB. Login falhou.")
            self._current_fernet_instance = None
            return False

        try:
            fernet_instance = self.cipher_manager.get_fernet_instance(master_password, stored_master_salt_hex)
            test_token = fernet_instance.encrypt(b"test_string_for_fernet_key_validation")
            fernet_instance.decrypt(test_token)

            self._current_fernet_instance = fernet_instance
            print("DEBUG SecurityService: Instância Fernet criada e armazenada com sucesso. Login BEM-SUCEDIDO.")
            return True
        except Exception as e:
            print(f"DEBUG SecurityService: Login FAILED (Exceção: {e}). _current_fernet_instance definido como None.")
            self._current_fernet_instance = None
            return False

    def save_password_entry(self, name: str, plain_password: str) -> bool:
        print(
            f"DEBUG SecurityService: save_password_entry chamado. _current_fernet_instance é {'válido' if self._current_fernet_instance else 'NULO'}.")
        if not self._current_fernet_instance:
            print("Erro: Faça login com a senha mestra primeiro para salvar senhas.")
            return False

        if not isinstance(name, str) or not name.strip():
            raise ValueError("O nome da senha não pode ser vazio.")

        encrypted_pwd = self.cipher_manager.encrypt_password(self._current_fernet_instance, plain_password)
        master_salt_for_entry = self.config_repo.get_setting(MASTER_SALT_SETTING_KEY)

        if not master_salt_for_entry:
            print("Erro interno: Salt da senha mestra não encontrado para salvar a entrada.")
            return False

        return self.repo.add(name, encrypted_pwd, master_salt_for_entry)

    def retrieve_password_by_name(self, name: str) -> str | None:
        print(
            f"DEBUG SecurityService: retrieve_password_by_name chamado. _current_fernet_instance é {'válido' if self._current_fernet_instance else 'NULO'}.")
        if not self._current_fernet_instance:
            print("Erro: Faça login com a senha mestra primeiro para recuperar senhas.")
            return None

        entry = self.repo.get_by_name(name)
        if not entry:
            print(f"DEBUG SecurityService: Entrada para '{name}' NÃO encontrada no repositório.")
            return None

        decrypted_pwd = self.cipher_manager.decrypt_password(self._current_fernet_instance, entry.encrypted_password)
        print(f"DEBUG SecurityService: Descriptografia de '{name}' resultou em: {decrypted_pwd is not None}.")
        return decrypted_pwd

    def get_all_password_entries_metadata(self) -> List[PasswordEntry]:
        return self.repo.get_all()

    def update_password_entry(self, entry_id: int, new_plain_password: str = None, new_name: str = None) -> bool:
        if not self._current_fernet_instance:
            print("Erro: Faça login com a senha mestra primeiro para atualizar senhas.")
            return False

        new_encrypted_pwd = None
        current_master_salt = self.config_repo.get_setting(MASTER_SALT_SETTING_KEY)

        if new_plain_password:
            new_encrypted_pwd = self.cipher_manager.encrypt_password(self._current_fernet_instance, new_plain_password)

        return self.repo.update(entry_id, new_name=new_name, new_encrypted_password=new_encrypted_pwd,
                                new_master_key_salt=current_master_salt)

    def delete_password_entry(self, entry_id: int) -> bool:
        """Deleta uma entrada de senha diretamente pelo seu ID."""
        return self.repo.delete(entry_id)

    def delete_password_by_name(self, name: str) -> bool:
        """
        Deleta uma entrada de senha com base no seu nome.
        """
        print(f"DEBUG SecurityService: Tentando deletar a senha com o nome: '{name}'")
        entry_to_delete = self.repo.get_by_name(name)

        if not entry_to_delete:
            print(f"DEBUG SecurityService: Senha com o nome '{name}' não encontrada. A exclusão falhou.")
            return False

        success = self.delete_password_entry(entry_to_delete.id)

        if success:
            print(f"DEBUG SecurityService: Senha com ID {entry_to_delete.id} ('{name}') deletada com sucesso.")
        else:
            print(f"DEBUG SecurityService: Falha ao deletar a senha com ID {entry_to_delete.id} no repositório.")
        return success
