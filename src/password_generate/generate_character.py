# PasswordGenerate/src/password_generate/generate_character.py

from src.password_generate.generate_number import generate_random_number

SPECIAL_CHARACTERS = ('/', ':', '!', '@', '#', '-', '+', '?', '$', '%', '&', '=', '*', '_')

def get_character() -> str:
    """
    Retorna um caractere especial aleatório de uma tupla de constantes.
    O índice para a seleção é gerado aleatoriamente e mapeado
    para garantir que todos os caracteres da tupla tenham uma chance.

    Returns:
        str: Um caractere especial aleatório.
    """

    value_index = generate_random_number()
    map_index = value_index % len(SPECIAL_CHARACTERS)
    return SPECIAL_CHARACTERS[map_index]