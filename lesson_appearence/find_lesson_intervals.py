"""
Небольшая программа для определения пересечения интервалов
присутствия ученика и учителя на уроке.

Для получения корректных результатов интервалы одного массива
должны быть ПРЕДВАРИТЕЛЬНО ОТСОРТИРОВАНЫ в порядке возрастания.

Т.к. интервалы представляют собой временные отрезки онлайн активности,
программа игнорирует подинтервалы интервалов одного массива.

Это сделано ввиду того, что, по моему мнению, невозможно присутствовать
онлайн одновременно в двух накладывающихся друг на друга интервалах.
Подинтервал (5, 7) непрерывного интервала (1, 10) не будет учтен.

По умолчанию программа предупреждает о наличии пересекающихся
интервалов в массиве и ожидает от пользователя дальнейших действий:
 - продолжить выпонление программы;
 - завершить выполнение программы.

Если вы не хотите получать предупреждение о наличии
пересекающихся интервалов, установите флаг `raise_overlap_exception`
функции `appearence` равным `False`.
"""
import sys
from typing import List, Sequence, Tuple


class IntervalsBaseException(Exception):
    """
    Базовый класс исключений,
    используемых в программе.
    """
    exception_description = 'Not implemented'

    def __init__(self, array_name: str) -> None:
        self.message = f'Массив `{array_name}` {self.exception_description}'
        super().__init__(self.message)


class IntervalOverlapException(IntervalsBaseException):
    """
    Исключение, вызываемое при пересечении
    интервалов в одном массиве.
    """
    exception_description = 'содержит пересекающиеся интервалы'


class EmptyArrayException(IntervalsBaseException):
    """
    Исключение, вызываемое при пустом массиве.
    """
    exception_description = 'пуст'


class OddArrayLengthException(IntervalsBaseException):
    """
    Исключение, вызываемое при массииве
    с нечетным количесвом элементов.
    """
    exception_description = 'содержит нечетное количество элементов'


def run_validation(
    *arrays: Sequence[Sequence[int]],
    raise_overlap_exception: bool
        ) -> None:
    """
    Выполнияет валидацию трех массивов.
    Передает имя массива в валидатор
    для более понятного вывода ошибок.

    "Накладка" интервалов одного массива
    является необязательной проверкой.
    """
    array_names = ('lesson', 'pupil', 'tutor')
    for array, array_name in zip(arrays, array_names):
        validate_empty_array(array, array_name)
        validate_even_array_length(array, array_name)
    if raise_overlap_exception:
        for array, array_name in zip(arrays, array_names):
            validate_overlap_intervals(array, array_name)


def validate_empty_array(array: Sequence[int], name: str) -> None:
    """Вызвать исключение, если массив пуст."""
    if not array:
        raise EmptyArrayException(name)


def validate_even_array_length(array: Sequence[int], name: str) -> None:
    """
    Вызвать исключение, если количество
    элементов в массиве нечетное.
    """
    if len(array) % 2:
        raise OddArrayLengthException(name)


def validate_overlap_intervals(array: Sequence[int], name: str) -> None:
    """
    Вызывать исключение, если в массиве
    есть пересекающиеся интервалы.
    """
    len_array = len(array)
    current_interval = array[:2]
    i = 2

    while i < len_array:
        if array[i] > current_interval[1]:
            current_interval = array[i:i+2]
            i += 2
        else:
            raise IntervalOverlapException(name)


def collect_lesson_intervals(
    lesson: Sequence[int],
    pupil: Sequence[int],
    tutor: Sequence[int]
        ) -> List[Tuple[int]]:
    """
    Поиск общих интервалов в массивах,
    содержащих временные отрезки урока, присутствия ученика и учителя.

    Значения массивов идут подряд в порядке возрастания.
    Четные элементы означают начало интервала, нечетные - конец.

    Пересечения в рамках одного массива игнорируются.
    """

    len_pupil = len(pupil)
    len_tutor = len(tutor)
    i = j = 0

    result = [(0, 0)]

    while i < len_pupil and j < len_tutor:
        # Проверяем, что интервалы пересекаются
        if pupil[i] <= tutor[j+1] and tutor[j] <= pupil[i+1]:
            start = max(pupil[i], tutor[j], lesson[0])
            end = min(pupil[i+1], tutor[j+1], lesson[1])

        # Перед добавлением нового интервала, проверяем
        # что он не входит в последний добавленный интервал.
            last_added_interval = result[-1]
            if not (
                start >= last_added_interval[0]
                and end <= last_added_interval[1]
            ):
                result.append((start, end))
            if pupil[i+1] > tutor[j+1]:    # Интервал Учителя закончился,
                j += 2                     # => ищем следующий интервал Учителя

            elif pupil[i+1] < tutor[j+1]:  # Интервал Ученика закончился,
                i += 2                     # => ищем следующий интервал Ученика
            else:
                i += 2                     # Интервалы закончились одномоментно
                j += 2                     # => находим два новых интервала.

        # Интервалы не пересекаются.   Интервал Ученика заканчивается полностью
        elif tutor[j] > pupil[i+1]:     # до начала интервала Учителя =>
            i += 2                      # переходим к новому интервау Ученика
        elif pupil[i] > tutor[j+1]:
            j += 2

    return result


def sum_intervals(intervals: List[Tuple[int]]):
    """
    Возвращает сумму длительности всех интервалов.
    """
    return sum(interval[1] - interval[0] for interval in intervals)


def appearence(
    lesson: Sequence[int],
    pupil: Sequence[int],
    tutor: Sequence[int],
    raise_overlap_exception: bool = True
        ) -> int:
    """
    Расчитывает продолжительность общих интервалов ученика и учителя.

    Перед рассчетом результатов проводится валидация входных массивов
    на наличие элементов и их четное количество.

    Флаг `raise_overlap_exception` указывает на необходимость
    валидации массивов на наличие подинтервалов, входящих в бóльшие интервалы.
    При наличии таких подинтервалов, будет предложено
    два варианта продолжения программы:
      - завершить выполнение;
      - продолжить выполнение (результаты могут отличаться от ожидаемых).
    """
    try:
        run_validation(
            lesson,
            pupil,
            tutor,
            raise_overlap_exception=raise_overlap_exception
        )
    except (EmptyArrayException, OddArrayLengthException) as validation_error:
        sys.exit(f"Ошибка валидации: {validation_error}.\n")
    except IntervalOverlapException as overlap_error:
        message = (
            f"{overlap_error}.\n"
            "Результаты вычсилений могут не совпадать с ожидаемыми.\n"
            "Чтобы продолжить нажмите любую кнопку. "
            "Нажмите ENTER чтобы выйти. "
        )
        proceed = input(message)
        if not proceed:
            sys.exit(0)

    lesson_intervals = collect_lesson_intervals(lesson, pupil, tutor)
    lesson_duration = sum_intervals(lesson_intervals)
    return f'Длительность общих интервалов: {lesson_duration} секунд(ы, а).'
