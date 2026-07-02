"""Módulo para cálculo da área de um círculo.

Este módulo disponibiliza funções e um script executável para calcular
a área de círculos de maneira precisa utilizando o módulo 'math'.
"""

import math

def calcular_area_circulo(raio):
    """Calcula a área de um círculo com base no valor de seu raio.

    Args:
        raio (float): O raio do círculo. Deve ser um valor não negativo.

    Returns:
        float: A área calculada do círculo.

    Raises:
        ValueError: Se o valor do raio for negativo.
    """
    if raio < 0:
        raise ValueError("O raio não pode ser negativo.")
    return math.pi * (raio ** 2)

if __name__ == '__main__':
    # Raio fixado em 10 para execução direta do módulo
    raio = 10.0

    # Bloco try-except para capturar exceções durante a execução direta do script
    try:
        area = calcular_area_circulo(raio)
        print(f"A área do círculo com raio {raio}\nÉ: {area:.4f}")
    except ValueError as e:
        # Exibe mensagens de erro amigáveis para entradas inválidas
        print(f"Erro: {e}")
