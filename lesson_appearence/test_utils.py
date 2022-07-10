import sys

from find_lesson_intervals import (
    EmptyArrayException,
    IntervalOverlapException,
    OddArrayLengthException,
    collect_lesson_intervals,
    run_validation,
    sum_intervals
)


def patched_appearence(
    lesson,
    pupil,
    tutor,
    proceed,
    raise_overlap_exception=True
):
    """ Измененная функция `appearence` для выполнения тестов. """
    try:
        run_validation(
            lesson,
            pupil,
            tutor,
            raise_overlap_exception=raise_overlap_exception
        )
    except (EmptyArrayException, OddArrayLengthException) as validation_error:
        sys.exit(f"Ошибка валидации: {validation_error}.\n")
    except IntervalOverlapException:
        proceed = proceed
        if not proceed:
            sys.exit(0)

    lesson_intervals = collect_lesson_intervals(lesson, pupil, tutor)
    lesson_duration = sum_intervals(lesson_intervals)
    return f'Длительность общих интервалов: {lesson_duration} секунд(ы, а).'
