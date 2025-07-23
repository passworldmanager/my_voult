# PythonPasswordGenerate/src/database/repositories/repository_config.py

import sqlite3
import os
from src.database.models.model_config import AppSetting
from src.config.path_config import DB_FILE_PATH, DB_DIRECTORY_PATH

class ConfigRepository:
    """
    Gerencia as operações de CRUD para as configurações da aplicação (AppSetting)
    no banco de dados SQLite.
    """

    def __init__(self):
        self.db_path = DB_FILE_PATH
        os.makedirs(DB_DIRECTORY_PATH, exist_ok=True)
        self.create_table()  # Chama a criação da tabela de configurações

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def create_table(self):
        """
        Cria a tabela 'app_settings' no banco de dados, se ela ainda não existir.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS app_settings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key TEXT NOT NULL UNIQUE,
                    value TEXT NOT NULL
                )
            """)

    def set_setting(self, key: str, value: str) -> bool:
        """
        Insere ou atualiza uma configuração na tabela 'app_settings'.
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT OR REPLACE INTO app_settings (key, value) VALUES (?, ?)", (key, value))
                conn.commit()
            return True
        except sqlite3.Error as e:
            return False

    def get_setting(self, key: str) -> str | None:
        """
        Recupera o valor de uma configuração da tabela 'app_settings'.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM app_settings WHERE key = ?", (key,))
            row = cursor.fetchone()
        if row:
            return row[0]
        return None

    def delete_setting(self, key: str) -> bool:
        """
        Deleta uma configuração específica pelo chave (key).
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM app_settings WHERE key = ?", (key,))
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            return False

