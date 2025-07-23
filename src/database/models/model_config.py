# PythonPasswordGenerate/src/database/models/model_config.py

class AppSetting:
    """
    Representa um par chave-valor para armazenar configurações da aplicação no banco de dados.
    """
    def __init__(self, id: int = None, key: str = None, value: str = None):
        self.id = id
        self.key = key
        self.value = value

    def __repr__(self):
        return f"AppSetting(id={self.id}, key='{self.key}', value='{self.value[:10]}...')"