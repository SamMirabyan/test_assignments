""" Тесты функции `appearence` модуля `lesson_appearence`. """

import unittest

from find_lesson_intervals import appearence
from test_utils import patched_appearence


class TestAppearence(unittest.TestCase):
    """ Набор тест-кейсов. """

    def setUp(self):
        self.empty_pupil = {
            'lesson': [0, 50],
            'pupil': [],
            'tutor': [20, 30, 40, 49]
        }
        self.odd_length_tutor = {
            'lesson': [0, 50],
            'pupil': [10, 20, 25, 45],
            'tutor': [20, 30, 40, 49, 50]
        }
        self.overlapping_pupil = {
            'lesson': [0, 50],
            'pupil': [10, 20, 25, 45, 30, 35],
            'tutor': [15, 30, 40, 49]
        }
        self.valid_arrays = {
            'lesson': [0, 100],
            'pupil': [10, 20, 25, 45, 46, 50, 55, 80, 83, 89, 90, 99],
            'tutor': [5, 30, 35, 70, 71, 88, 89, 105]
        }
        self.very_short_lesson = {
            'lesson': [0, 25],
            'pupil': [10, 20, 25, 45],
            'tutor': [15, 30, 40, 49]
        }
        return super().setUp()

    def test_empty_array(self):
        """
        При передаче пустового массива
        выполняется выход из программы
        с выводом нужного предупреждения.
        """
        error_message = 'Ошибка валидации: Массив `pupil` пуст.\n'
        with self.assertRaises(SystemExit) as exit_info:
            appearence(**self.empty_pupil)
        self.assertEqual(
            exit_info.exception.code,
            error_message,
            msg=(
                'Убедитесь, что при передаче пустого массива выполняется '
                'выход из программы с выводом нужного предупреждения.'
            )
        )

    def test_odd_length_array(self):
        """
        При передаче массива с нечетным количеством
        элементов выполняется выход из программы
        с выводом нужного предупреждения.
        """
        error_message = (
            'Ошибка валидации: Массив `tutor` содержит '
            'нечетное количество элементов.\n'
        )
        with self.assertRaises(SystemExit) as exit_info:
            appearence(**self.odd_length_tutor)
        self.assertEqual(
            exit_info.exception.code,
            error_message,
            msg=(
                'Убедитесь, что при передаче массива с нечетным количеством '
                'элементов выполняется выход из программы '
                'с выводом нужного предупреждения'
            )
        )

    def test_valid_arrays(self):
        """
        При передаче валидных массивов
        выполняется расчет интервалов
        и вывод результата в нужном формате.
        """
        expected_result = 'Длительность общих интервалов: 67 секунд(ы, а).'
        self.assertEqual(
            expected_result,
            appearence(**self.valid_arrays),
            msg=(
                'Убедитесь, что при передаче валидных массивов '
                'программа правильно считает сумму интервалов '
                'и выводит результат в заданном формате.'
            )
        )

    def test_deactivate_overlap_exception(self):
        """
        При передаче массива с `накладывающимися` интервалами,
        флаг `raise_overlap_exception=False` предотвращает
        вызов предупреждения. Выполяется расчет интервалов
        и вывод результата в нужном формате.
        """
        expected_result = 'Длительность общих интервалов: 15 секунд(ы, а).'
        self.assertEqual(
            expected_result,
            appearence(
                **self.overlapping_pupil,
                raise_overlap_exception=False
            ),
            msg=(
                'Убедитесь, что флаг `raise_overlap_exception=False` '
                'предотвращает вызов предупреждения при передаче массива '
                'с `накладывающимися` интервалами.'
            )
        )

    def test_exit_if_overlap_exception(self):
        """
        Программа должна завершиться системным выходом,
        если при получении предупреждения о `накладывающихся` интервалах
        пользователь решит прервать выполнение программы.
        """
        exit_code = 0
        with self.assertRaises(SystemExit) as exit_info:
            patched_appearence(**self.overlapping_pupil, proceed=False)
        self.assertEqual(
            exit_info.exception.code,
            exit_code,
            msg=(
                'Убедитесь, что при передаче пустой строки во время '
                'обработки предупреждения о `накладывающихся` интервалах '
                'выполняется выход из программы с нужным кодом.'
            )
        )

    def test_continue_if_overlap_exception(self):
        """
        Программа должна вернуть результат вычислений,
        если при получении предупреждения о `накладывающихся` интервалах
        пользователь решит продолжить выполнение программы.
        """
        expected_result = 'Длительность общих интервалов: 15 секунд(ы, а).'
        self.assertEqual(
            expected_result,
            patched_appearence(**self.overlapping_pupil, proceed=True),
            msg=(
                'Убедитесь, что при передаче НЕпустой строки во время '
                'обработки предупреждения о `накладывающихся` интервалах '
                'программа продолжает выполнение и возвращает результат.'
            )
        )


if __name__ == '__main__':
    unittest.main()
