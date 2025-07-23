# PasswordGenerate/src/password_generate/generate_number.py

import random

def generate_random_number() -> int:
    """
    Função que gera um número randomico de (0) até (25) incluido.
    :return:
    """
    return random.randint(0, 25)
