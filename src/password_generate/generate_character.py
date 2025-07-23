# PasswordGenerate/src/password_generate/generate_character.py

from src.password_generate.generate_number import generate_random_number

SPECIAL_CHARACTERS = ['/', ':', '!', '@', '#', '-', '+', '?', '$', '%', '&', '=', '*', '_']

def get_character() -> str:
    """
    Retorna um caractere especial aleatório de uma lista.
    O índice para a seleção é gerado aleatoriamente e mapeado
    para garantir que todos os caracteres da lista tenham uma chance.

    Returns:
        str: Um caractere especial aleatório.
    """
    value_index = generate_random_number()
    # Usar o operador módulo para mapear o índice para o tamanho da lista de caracteres especiais.
    # Isso garante que todos os caracteres de SPECIAL_CHARACTERS podem ser selecionados.
    map_index = value_index % len(SPECIAL_CHARACTERS)
    return SPECIAL_CHARACTERS[map_index]