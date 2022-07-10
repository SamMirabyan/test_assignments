"""
Набор тестов для функций нахождения первого нуля в строке:
 - find_first_zero_builtin;
 - find_first_zero_with_re.
"""

import unittest

from find_first_zero import find_first_zero_builtin, find_first_zero_with_re


def make_tests(func: callable) -> unittest.TestCase:
    """ Фабрика тест-кейсов для разных версий функции. """

    class TestFindFirstZero(unittest.TestCase):
        """ Набор тест-кейсов. """

        def setUp(self):
            self.no_zero = '11111111111111111111'
            self.first_zero = '01111111111111111111'
            self.last_zero = '11111111111111111110'
            self.only_zero = '00000000000000000000'
            self.random_zero = '10100101110010101100'
            self.empy_string = ''
            return super().setUp()

        def test_no_zero(self):
            expected_result = 'Строка не содержит нулей.'
            self.assertEqual(
                func(self.no_zero),
                expected_result,
                msg=(
                    f'Убедитесь, что функция `{func.__code__.co_name}` '
                    'правильно обрабатывает строку без нулей'
                )
            )

        def test_first_zero(self):
            expected_index = 0
            expected_result = f'Индекс первого нуля: {expected_index}.'
            self.assertEqual(
                func(self.first_zero),
                expected_result,
                msg=(
                    f'Убедитесь, что функция `{func.__code__.co_name}` '
                    'правильно обрабатывает строку, начинающуюся с нуля'
                )
            )

        def test_last_zero(self):
            expected_index = 19
            expected_result = f'Индекс первого нуля: {expected_index}.'
            self.assertEqual(
                func(self.last_zero),
                expected_result,
                msg=(
                    f'Убедитесь, что функция `{func.__code__.co_name}` '
                    'правильно обрабатывает строку, оканчивающуюся нулем'
                )
            )

        def test_only_zero(self):
            expected_index = 0
            expected_result = f'Индекс первого нуля: {expected_index}.'
            self.assertEqual(
                func(self.only_zero),
                expected_result,
                msg=(
                    f'Убедитесь, что функция `{func.__code__.co_name}` '
                    'правильно обрабатывает строку, содержащую только нули'
                )
            )

        def test_random_zero(self):
            expected_index = 1
            expected_result = f'Индекс первого нуля: {expected_index}.'
            self.assertEqual(
                func(self.random_zero),
                expected_result,
                msg=(
                    f'Убедитесь, что функция `{func.__code__.co_name}` '
                    'правильно обрабатывает смешанную строку из единиц и нулей'
                )
            )

        def test_empty_string(self):
            expected_result = 'Строка не содержит нулей.'
            self.assertEqual(
                func(self.empy_string),
                expected_result,
                msg=(
                    f'Убедитесь, что функция `{func.__code__.co_name}` '
                    'правильно обрабатывает пустую строку'
                )
            )

    return TestFindFirstZero


class TestStringFindMethod(make_tests(find_first_zero_builtin)):
    """ Тесты для фнукции, использующей str.find метод. """
    pass


class TestRegExp(make_tests(find_first_zero_with_re)):
    """ Тесты для функции, использующей регулярные выражения. """
    pass


if __name__ == '__main__':
    unittest.main()
