"""
Программа подсчета количества названий животных
на русском языке на Википедии в категории `Животные по алфавиту`.

Общий поток выполенения:
1. Получить тектсовое содержание страницы с помощью `requests`.
2. С помощью `beautifulsoup` получить HTML элементы:
  - буква алфавита (<h3>);
  - список ссылок на страницы животных под буквой (<li>);
  - ссылку на следующую страницу (<a>).
3. Количество ссылок добавить к счетчику.
4. Повторять, пока не будет найден первый ASCII символ,
   т.е. первая буква английского алфавита.
"""

import sys
import requests
from collections import Counter
from pprint import pprint
from bs4 import BeautifulSoup


class CounterLoadedException(Exception):
    """ Исключение повторной загрузки данных при заполненном Счетчике. """
    def __init__(self):
        self.message = (
            'Счетчик содержит данные. Для повтороного запуска Счетчика'
            'воспользуйтесь методом `reload`'
        )
        super().__init__(self.message)


class BaseWikiAnimalNameCounter:
    """
    Базовый класс. Содержит основной функционал
    обработки страниц и подсчета количества названий животных.
    Не используется напрямую, т.к. не имеет интерфейса.
    """
    BASE_URL = (
        'https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1'
        '%80%D0%B8%D1%8F:%D0%96%D0%B8%D0%B2%D0%BE%D1%82%D0%BD%D1%8B%D0%B5_%D0%'
        'BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83'
    )
    CONNECTION_ERROR_MESSAGE = (
        'Ваш запрос не может быть обработан. '
        'Проверьте правильность URL адреса или интернет соединение'
    )
    FIRST_LETTER = 'А'
    IMPROPER_USE_MESSAGE = (
        'Класс {} нельзя использовать напрямую. '
        'Создайте дочерний класс и реализуйте необходимые методы.'
    )
    WIKI_DOMAIN = 'https://ru.wikipedia.org'

    def __init__(self) -> None:
        self._counter = Counter()
        self.loaded = False

    def load(self):
        raise NotImplementedError(
            self.IMPROPER_USE_MESSAGE.format(self.__class__.__name__)
        )

    def reload(self):
        raise NotImplementedError(
            self.IMPROPER_USE_MESSAGE.format(self.__class__.__name__)
        )

    def total(self):
        raise NotImplementedError(
            self.IMPROPER_USE_MESSAGE.format(self.__class__.__name__)
        )

    def size(self):
        raise NotImplementedError(
            self.IMPROPER_USE_MESSAGE.format(self.__class__.__name__)
        )

    def keys(self):
        raise NotImplementedError(
            self.IMPROPER_USE_MESSAGE.format(self.__class__.__name__)
        )

    def values(self):
        raise NotImplementedError(
            self.IMPROPER_USE_MESSAGE.format(self.__class__.__name__)
        )

    def items(self):
        raise NotImplementedError(
            self.IMPROPER_USE_MESSAGE.format(self.__class__.__name__)
        )

    def _clear(self):
        raise NotImplementedError(
            self.IMPROPER_USE_MESSAGE.format(self.__class__.__name__)
        )

    def print(self, by_value=False):
        raise NotImplementedError(
            self.IMPROPER_USE_MESSAGE.format(self.__class__.__name__)
        )

    def _count_letters(self):
        """
        Подсчитывает количество названий животных
        с группировкой по буквам русского алфавита.
        """
        current_letter = self.FIRST_LETTER
        current_url = self.BASE_URL

        print(f'Обрабатываю животных на букву {current_letter}')
        while not current_letter.isascii():
            contents = self._get_page_contents(current_url)
            soup = BeautifulSoup(contents, 'lxml')
            animal_list = soup.find('div', 'mw-category-columns').contents
            for animal in animal_list:
                first_animal_letter = animal.find('h3').text.upper()

                #  Случай, когда на одной странице встречаются категории
                #  животных на русском и английском языках.
                if first_animal_letter.isascii():
                    break

                if first_animal_letter != current_letter:
                    print(
                        f'Обрабатываю животных на букву {first_animal_letter}'
                    )
                list_elements = animal.find_all('li')
                self._counter[first_animal_letter] += len(list_elements)
            current_letter = first_animal_letter
            current_url = self._get_next_page_url(soup)

    def _get_page_contents(self, url):
        """ Возвращает текстовое содержание web-страницы. """
        try:
            contents = requests.get(url).text
        except requests.exceptions.ConnectionError:
            sys.exit(self.CONNECTION_ERROR_MESSAGE)
        return contents

    def _get_next_page_url(self, soup):
        """ Находит и возвращает ссылку на следующую страницу. """
        prev_next_pages = soup.find(
            'div', attrs={'id': 'mw-pages'}
        ).find_all(
            'a', attrs={'title': 'Категория:Животные по алфавиту'}
        )
        for page in prev_next_pages:
            if page.text == 'Следующая страница':
                end_point = page.get('href')
                return self.WIKI_DOMAIN + end_point
        sys.exit(
            'Структура страницы сайта была изменена! Обратитесь к разработчику'
        )


class WikiAnimalNameCounter(BaseWikiAnimalNameCounter):
    """ Класс `Счетчика`, реализующий основной интерфейс. """

    def load(self):
        """ Запустить счетчик. Повторный запуск не допусается. """
        if self.loaded:
            raise CounterLoadedException()
        self._count_letters()
        self.loaded = True

    def reload(self):
        """ Повторный запуск Счетчика с предварительной очисткой данных. """
        self._clear()
        self.load()

    @property
    def total(self):
        """ Получить общее количество названий животных. """
        return sum(value for value in self._counter.values())

    @property
    def size(self):
        """ Получить количество обработанных букв. """
        return len(self._counter)

    def keys(self):
        """
        Получить все обработанные буквы.
        Дублирует collections.Counter().keys().
        """
        return self._counter.keys()

    def values(self):
        """
        Получить все значения.
        Дублирует collections.Counter().values().
        """
        return self._counter.values()

    def items(self):
        """
        Получить кортежи букв их количественных значений.
        Дублирует collections.Counter().items().
        """
        return self._counter.items()

    def _clear(self):
        """ Очистить Счетчик. Дублирует collections.Counter().clear(). """
        self._counter.clear()

    def print(self, by_value=False):
        """ Форматированный вывод содержимого Счетчика. """
        print('Количество животных ', end='')

        if by_value:
            print('(сортировка по количеству): ')
            pprint(self._counter)
        else:
            print('(сортировка по алфавиту): ')
            pprint(dict(self._counter.items()))


if __name__ == '__main__':
    counter = WikiAnimalNameCounter()
    counter.load()
    print('\n')
    counter.print()
