# PasswordGenerate/src/password_generate/generate_hexadecimal.py

from src.password_generate.generate_number import generate_random_number

def generate_hexadecimal_value() -> str:
    """
    Gera um valor hexadecimal de 2 dígitos a partir de um valor randômico.
    O valor randômico (0-25) é convertido para sua representação hexadecimal.

    Returns:
        str: Uma string hexadecimal de 2 dígitos (ex: '0A', '19').
    """
    decimal_value = generate_random_number()
    return f"{decimal_value:02X}"