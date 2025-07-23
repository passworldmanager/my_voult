# PasswordGenerate/src/config/path_config.py

import os
import sys

DB_DIRECTORY_NAME = "data"

DB_FILENAME = "passwords.db"

def get_resource_path(relative_path: str) -> str:
    """
    Retorna o caminho absoluto para o recurso, funcionando tanto no modo de
    desenvolvimento quanto em um aplicativo empacotado pelo PyInstaller.
    """
    try:
        # PyInstaller cria uma pasta temporária e armazena o caminho em _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # Se não estiver empacotado, usa o caminho absoluto do diretório raiz do projeto
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

DB_DIRECTORY_PATH = get_resource_path(DB_DIRECTORY_NAME)

DB_FILE_PATH = os.path.join(DB_DIRECTORY_PATH, DB_FILENAME)