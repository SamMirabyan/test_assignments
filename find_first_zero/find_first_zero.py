"""
Программа для поиска первого нуля
в строке, состоящей из нулей и единиц.

Возвращает индекс первого нуля.
"""

import re


def find_first_zero_builtin(ones_and_zeros: str) -> int:
    """
    Находит индекс первого символа равного '0'.
    """
    if (index := ones_and_zeros.find('0')) >= 0:
        return f'Индекс первого нуля: {index}.'
    return 'Строка не содержит нулей.'


def find_first_zero_with_re(ones_and_zeros: str) -> int:
    """
    Находит индекс, следующий за искомым паттерном.
    Вычитаем единицу, чтобы вернуться к первому нулю.
    """
    if contains_zeros := re.match('1*0', ones_and_zeros):
        index = contains_zeros.end() - 1
        return f'Индекс первого нуля: {index}.'
    return 'Строка не содержит нулей.'
