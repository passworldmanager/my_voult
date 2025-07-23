# PasswordGenerate/src/password_generate/generate_uppercase_letters.py

from src.password_generate.generate_number import generate_random_number
import string

def get_uppercase_letter() -> str:
    """
    Esta função retorna uma letra maiúscula aleatória.
    Ela utiliza um valor aleatório gerado pela função 'generate_random_number'
    para selecionar uma letra no índice do alfabeto maiúsculo.

    Returns:
        str: Uma letra maiúscula aleatória (A-Z).
    """
    index_value = generate_random_number()
    return string.ascii_uppercase[index_value]