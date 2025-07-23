# PythonPasswordGenerate/src/database/repositories/repository.py

import sqlite3
import os
from src.database.models.model import PasswordEntry
from src.config.path_config import DB_FILE_PATH, DB_FILENAME, DB_DIRECTORY_NAME, DB_DIRECTORY_PATH


class PasswordRepository:
    """
    Gerencia as operações de CRUD para as entradas de senha (PasswordEntry)
    no banco de dados SQLite.
    """
    def __init__(self):
        self.db_path = DB_FILE_PATH
        os.makedirs(DB_DIRECTORY_PATH, exist_ok=True)
        self.create_table() # Chama a criação da tabela de senhas

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def create_table(self):
        """
        Cria a tabela 'password_entries' no banco de dados, se ela ainda não existir.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS password_entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    encrypted_password TEXT NOT NULL,
                    master_key_salt TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

    def add(self, name: str, encrypted_password: str, master_key_salt: str) -> bool:
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO password_entries (name, encrypted_password, master_key_salt)
                    VALUES (?, ?, ?)
                """, (name, encrypted_password, master_key_salt))
                conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        except sqlite3.Error as e:
            return False

    def get_by_name(self, name: str) -> PasswordEntry | None:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, encrypted_password, master_key_salt, created_at FROM password_entries WHERE name = ?", (name,))
            row = cursor.fetchone()
        if row:
            return PasswordEntry(id=row[0], name=row[1], encrypted_password=row[2], master_key_salt=row[3], created_at=row[4])
        return None

    def get_all(self) -> list[PasswordEntry]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, encrypted_password, master_key_salt, created_at FROM password_entries ORDER BY name")
            rows = cursor.fetchall()
        return [PasswordEntry(id=row[0], name=row[1], encrypted_password=row[2], master_key_salt=row[3], created_at=row[4]) for row in rows]

    def update(self, entry_id: int, new_name: str = None, new_encrypted_password: str = None, new_master_key_salt: str = None) -> bool:
        conn = self._get_connection()
        cursor = conn.cursor()
        update_fields = []
        params = []

        if new_name is not None:
            update_fields.append("name = ?")
            params.append(new_name)
        if new_encrypted_password is not None:
            update_fields.append("encrypted_password = ?")
            params.append(new_encrypted_password)
        if new_master_key_salt is not None:
            update_fields.append("master_key_salt = ?")
            params.append(new_master_key_salt)

        if not update_fields:
            return False

        params.append(entry_id)
        query = f"UPDATE password_entries SET {', '.join(update_fields)} WHERE id = ?"

        try:
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.IntegrityError:
            return False
        except sqlite3.Error as e:
            return False
        finally:
            conn.close()

    def delete(self, entry_id: int) -> bool:
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM password_entries WHERE id = ?", (entry_id,))
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            return False
