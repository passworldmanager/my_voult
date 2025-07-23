# PasswordGenerate/src/password_generate/generate_lowercase_letters.py

from src.password_generate.generate_number import generate_random_number
import string

def get_lowercase_letters() -> str:
    """
    Esta função retorna uma letra minúscula aleatória do alfabeto.
    Ela utiliza um valor aleatório gerado pela função 'generate_random_number'
    para selecionar uma letra no índice do alfabeto minúsculo.

    Returns:
        str: Uma letra minúscula aleatória (a-z).
    """
    index_value = generate_random_number()
    return string.ascii_lowercase[index_value]