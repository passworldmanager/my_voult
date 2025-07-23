# PasswordGenerate/src/password_generate/password_generator.py

import random
from src.password_generate.generate_character import get_character
from src.password_generate.generate_hexadecimal import generate_hexadecimal_value
from src.password_generate.generate_lowercase_letters import get_lowercase_letters
from src.password_generate.generate_uppercase_letters import get_uppercase_letter

def password_generator() -> str:
    """
    Gera uma senha com 13 caracteres aleatórios, combinando diferentes tipos
    (letras maiúsculas, minúsculas, caracteres especiais e valores hexadecimais).

    Returns:
        str: A senha gerada.
    """
    password_parts = []

    generators = [
        get_uppercase_letter,
        get_lowercase_letters,
        get_character,
        generate_hexadecimal_value
    ]

    generated_chars = []
    current_length = 0

    while current_length < 13:
        chosen_generator = random.choice(generators)

        new_char_or_hex = chosen_generator()

        if chosen_generator == generate_hexadecimal_value:
            # Se for hexadecimal, ele já tem 2 chars, então adicionamos ambos
            generated_chars.append(new_char_or_hex[0])
            generated_chars.append(new_char_or_hex[1])
            current_length += 2
        else:
            generated_chars.append(new_char_or_hex)
            current_length += 1

        # Limita a 13 caracteres
        if current_length > 13:
            generated_chars = generated_chars[:13]
            current_length = 13

    return "".join(generated_chars)

print(f"Senha gerada: {password_generator()}")
print(f"Senha gerada (segunda vez): {password_generator()}")  # Testa se gera diferente agora