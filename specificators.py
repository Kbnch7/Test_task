# Паттерн Specification
class Specification:
    def is_satisfied(self, book):
        pass


class AuthorSpecification(Specification):
    def __init__(self, author):
        self.__specificator = author

    def is_satisfied(self, book):
        return self.__specificator == book.author


class TitleSpecification(Specification):
    def __init__(self, title):
        self.__specificator = title

    def is_satisfied(self, book):
        return self.__specificator == book.title


class YearSpecification(Specification):
    def __init__(self, year):
        self.__specificator = year

    def is_satisfied(self, book):
        return self.__specificator == book.year
