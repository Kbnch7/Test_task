import json

from specificators import Specification


# Класс книги
class Book:
    def __init__(self, id: int, title: str, author: str, year: int):
        self.__id = id
        self.__title = self.__set_title(title)
        self.__author = self.__set_author(author)
        self.__year = self.__set_year(year)
        self.__status = "avalible"

    def __str__(self):
        return ', '.join(
                        [str(self.__id),
                         self.__title,
                         self.__author,
                         str(self.__year),
                         self.__status])

    # Инициализаторы переменной
    def __set_title(self, title: str):
        if not isinstance(title, str):
            raise TypeError("Название книги должно быть строкой.")
        return title

    def __set_author(self, author: str):
        if not isinstance(author, str):
            raise TypeError("Фамилия автора должна быть строкой.")
        return author

    def __set_year(self, year: str):
        if not isinstance(year, int):
            raise TypeError("Год выпуска должен быть целым числом.")
        return year

    # Геттеры.
    @property
    def id(self):
        return self.__id

    @property
    def title(self):
        return self.__title

    @property
    def author(self):
        return self.__author

    @property
    def year(self):
        return self.__year

    @property
    def status(self):
        return self.__status

    # Сеттеры.
    @status.setter
    def status(self, new_status):
        if new_status not in ('avalible', 'unavalible'):
            raise ValueError('Неверное значение статуса.')
        self.__status = new_status


# Функция, которая распаковывает данные из json файла.
def decode_json(json_name: str = None):
    FILE_NAME_TYPE_ERROR = "Название файла должно быть строкой."
    FILE_NOT_FOUND_ERROR = "Указанный файл не найден. Будет создан новый файл."
    if not isinstance(json_name, str):
        raise TypeError(FILE_NAME_TYPE_ERROR)
    try:
        with open(json_name, 'r', encoding='utf-8') as f:
            data = json.load(f)
            increment = data['increment']
            books = [Book(book['id'],
                          book['title'],
                          book['author'],
                          book['year']) for book in data['books'].values()]
            return increment, books
    except FileNotFoundError:
        print(FILE_NOT_FOUND_ERROR)
        open(json_name, 'w', encoding='utf-8').close()
        return 0, []


# Класс библиотеки
class Library:
    __SUCCESS_ADD = "Книга с названием '{}', "\
                    "автора {} и годом выпуска {} успешно добавлена."
    __SUCCESS_DELETE = "Книга с названием '{}', "\
                       "автора {} и годом выпуска {} успешно удалена."
    __FAILED_DELETE = "Книга с id={} не найдена."
    __increment = 0

    def __init__(self, json_name: str):
        Library.__increment, self.__books = decode_json(json_name)
        self.__source = json_name

    @property
    def source(self):
        return self.__source

    # Метод добавления книги в библиотеку.
    def add(self, title: str, author: str, year: int):
        self.__books.append(Book(Library.__increment, title, author, year))
        print(self.__SUCCESS_ADD.format(title, author, year))
        Library.__increment += 1

    # Метод удаления книги из библиотеки.
    def delete(self, id: int):
        for index, book in enumerate(self.__books):
            if book.id == id:
                deleted_book = self.__books.pop(index)
                print(self.__SUCCESS_DELETE.format(
                        deleted_book.title,
                        deleted_book.author,
                        deleted_book.year))
                break
        else:
            print(self.__FAILED_DELETE.format(id))

    # Метод поиска книг по спецификатору.
    def find(self, specification: Specification):
        res = []
        for book in self.__books:
            if specification.is_satisfied(book):
                res.append(book)
        print('\n'.join([str(book) for book in res]))

    # Метод вывода всех книг.
    def show_all(self):
        for book in self.__books:
            print(book)

    # Метод изменения статуса книги.
    def change_status(self, id, new_status):
        for index, book in enumerate(self.__books):
            if book.id == id:
                self.__books[index].status = new_status
                break

    # Функция сохранения изменений.
    def save(self):
        with open(self.__source, 'w', encoding='utf-8') as f:
            books = {str(book.id): {
                'id': book.id,
                'title': book.title,
                'author': book.author,
                'year': book.year,
                'status': book.status
            } for book in self.__books}
            json.dump(
                {'increment': self.__increment, 'books': books},
                f,
                ensure_ascii=False,
                indent=4)
