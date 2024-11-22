from utils import Library
from specificators import AuthorSpecification, TitleSpecification, YearSpecification

HELLO_MESSAGE = 'Введите название файла библиотеки чтобы '\
                'открыть интерфейс работы с ним: '
INSTRUCTIONS_MESSAGE = \
    'Для добавления книги воспользуйтесь командой '\
    '<add *Название книги в двойных кавычках* *Автор* *Год выпуска*>\n'\
    'Для удаления книги воспользуйтесь командой '\
    '<delete *id книги*>\n'\
    'Для поиска книги воспользуйтесь командой '\
    '<find *фильтр поиска(title/author/year)*=*значение фильтра*>\n'\
    'Для отображения всех книг воспользуйтесь командой '\
    '<show_all>\n'\
    'Для изменения статуса книги воспользуйтесь командой '\
    '<change_status *id книги* *новый статус (avalible/unavalible)*>\n'\
    'Для сохранения изменений воспользуйтесь командой '\
    '<save>\n'\
    'Для выхода из программы воспользуйтесь командой <quit>'
TOO_MANY_ARGUMENTS_ERROR = 'Неверное количество аргументов'
WRONG_DATATYPE_ID = 'Данные введены неверно (id должен быть целым цислом)'
WRONG_DATATYPE_YEAR = 'Данные введены неверно '\
                        '(year должен быть целым числом)'


# Валидация входных данных для функции добавления книги.
def validate_add_message(msg):
    UNCLOSED_QUOTES_ERROR = 'Данные введены неверно (" не закрыта)'
    title = [msg[1]]
    if msg[1].count('"') != 2:
        for index in range(2, len(msg)):
            title.append(msg[index])
            if msg[index].count('"'):
                author = msg[index+1]
                year = msg[index+2]
                if index+3 != len(msg):
                    raise ValueError(TOO_MANY_ARGUMENTS_ERROR)
                break
        else:
            raise ValueError(UNCLOSED_QUOTES_ERROR)
    else:
        if len(msg) != 4:
            raise ValueError(TOO_MANY_ARGUMENTS_ERROR)
        author = msg[2]
        year = msg[3]
    if not year.isdigit():
        raise ValueError(WRONG_DATATYPE_YEAR)
    title = title[0][1:-1] if len(title) == 1 else title[1:-1]
    return [title, author, int(year)]


# Валидация входных данных для функции удаления книги.
def validate_delete_message(msg):
    if len(msg) != 2:
        raise ValueError(TOO_MANY_ARGUMENTS_ERROR)
    if not msg[1].isdigit():
        raise ValueError(WRONG_DATATYPE_ID)
    return int(msg[1])


# Валидация входных данных для функции поиска книги.
def validate_find_message(msg):
    SPECIFICATORS_ERROR = 'Данные введены неверно '\
                    '(фильтр должен быть равен одному из title/author/year)'
    WRONG_TITLE_FORMAT = 'Данные введены неверно '\
                         '(название должно быть в двойных кавычках)'
    SPECIFICATORS = ('title', 'author', 'year')
    if len(msg) != 2:
        raise ValueError(TOO_MANY_ARGUMENTS_ERROR)
    specification = msg[1].split('=')
    if specification[0] not in SPECIFICATORS:
        raise ValueError(SPECIFICATORS_ERROR)

    if specification[0] == 'title':
        if specification[1].count('"') != 2:
            raise ValueError(WRONG_TITLE_FORMAT)
        return TitleSpecification(specification[1][1:-1])
    elif specification[0] == 'author':
        return AuthorSpecification(specification[1])
    else:
        if not specification[1].isdigit():
            raise ValueError(WRONG_DATATYPE_YEAR)
        return YearSpecification(int(specification[1]))


# Функция для вывода всех книг.
def show_all(library, msg):
    if len(msg) != 1:
        raise ValueError(TOO_MANY_ARGUMENTS_ERROR)
    library.show_all()


# Валидация входных данных для функции изменения статуса книги.
def validate_change_status(msg):
    STATUS_VALUE_ERROR = 'Данные введены неверно (статус может быть равен avalible/unavalible)'
    statuses = ('avalible', 'unavalible')
    if len(msg) != 3:
        raise ValueError(TOO_MANY_ARGUMENTS_ERROR)
    if msg[2] not in statuses:
        raise ValueError(STATUS_VALUE_ERROR)
    if not msg[1].isdigit():
        raise ValueError(WRONG_DATATYPE_ID)
    return [int(msg[1]), msg[2]]


# Валидация входных данных для функции сохранения результата.
def validate_save(msg):
    if len(msg) != 1:
        raise ValueError(TOO_MANY_ARGUMENTS_ERROR)


# Основной цикл программы.
if __name__ == '__main__':
    json_name = input(HELLO_MESSAGE)
    lib = Library(json_name)
    print(INSTRUCTIONS_MESSAGE)
    print(f'{lib.source}> ', end='')
    message = list(map(str, input().split()))
    while message != ['quit']:
        if not message:
            message = list(map(str, input().split()))
            continue
        if message[0] == 'add':
            data = validate_add_message(message)
            lib.add(*data)
        elif message[0] == 'delete':
            id = validate_delete_message(message)
            lib.delete(id)
        elif message[0] == 'find':
            specificator = validate_find_message(message)
            lib.find(specificator)
        elif message[0] == 'show_all':
            show_all(lib, message)
        elif message[0] == 'change_status':
            data = validate_change_status(message)
            lib.change_status(*data)
        elif message[0] == 'save':
            validate_save(message)
            lib.save()

        print(f'{lib.source}> ', end='')
        message = list(map(str, input().split()))
