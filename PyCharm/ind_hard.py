#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys
import os
import jsonschema
from jsonschema import validate


def get_way():
    """
    Запросить данные о маршруте.
    """
    start = input('Название начального маршрута: ')
    finish = input('Название конечного маршрута: ')
    num = int(input('Номер маршрута: '))

    # Вернуть словарь.
    return {
        'start': start,
        'finish': finish,
        'num': num,
    }


def display_way(numbers):
    """
    Отобразить список маршрутов.
    """
    if numbers:
        # Заголовок таблицы.
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 30,
            '-' * 15
        )
        print(line)
        print(
            '| {:^4} | {:^30} | {:^30} | {:^15} |'.format(
                "No",
                "Название начального маршрута",
                "Название конечного маршрута",
                "Номер маршрута"
            )
        )
        print(line)

        # Вывести данные о всех маршрутах.
        for idx, way in enumerate(numbers, 1):
            print(
                '| {:>4} | {:<30} | {:<30} | {:>15} |'.format(
                    idx,
                    way.get('start', ''),
                    way.get('finish', ''),
                    way.get('num', 0)
                )
            )
        print(line)

    else:
        print("Список пуст.")


def find_way(numbers, nw):
    """
    Выбрать маршрут с данным номером.
    """
    # Список маршрутов
    result = []
    for h in numbers:
        if nw in str(h.values()):
            result.append(h)
    # Возвратить список выбранных маршрутов.
    return result


def save_ways(file_name, routes):
    """
    Сохранить номера всех маршрутов в файл JSON.
    """
    # Открыть файл с заданным именем для записи.
    with open(file_name, "w", encoding="utf-8") as fout:
        # Выполнить сериализацию данных в формат JSON.
        # Для поддержки кирилицы установим ensure_ascii=False
        json.dump(routes, fout, ensure_ascii=False, indent=4)


def load_ways(file_name, load):
    os.chdir("/Users/svetik/Desktop/OPI/OPI_LR_2.16")
    """
    Загрузить все маршруты из файла JSON.
    """
    # Открыть файл с заданным именем для чтения.
    with open(file_name, "r", encoding="utf-8") as fin:
        return json.load(fin)
    print("Файл загружен")
    validate(file, load)
    return file


def validate(file, schema):
    validator = jsonschema.Draft7Validator(schema)
    try:
        if not validator.validate(file):
            print("Нет ошибок валидации")
    except jsonschema.exceptions.ValidationError:
        print("Ошибка валидации", file=sys.stderr)
        exit(1)


def main():
    """
    Главная функция программы.
    """
    os.chdir("/Users/svetik/Desktop/OPI/OPI_LR_2.16")
    with open('check.json', 'r') as check:
        first_load = json.load(check)
    # Маршруты
    ways = []

    # Организовать бесконечный цикл запроса команд.
    while True:
        # Запросить команду из терминала.
        command = input(">>> ").lower()

        # Выполнить действие в соответствие с командой.
        if command == 'exit':
            break

        elif command == 'add':
            # Запросить данные о маршруте.
            way = get_way()

            # Добавить словарь в список.
            ways.append(way)
            # Отсортировать список в случае необходимости.
            if len(ways) > 1:
                ways.sort(key=lambda item: item.get('num', 0))

        elif command == 'list':
            # Отобразить все маршруты.
            display_way(ways)

        elif command == 'find':
            f = command.split('Введите номер маршрута: ', maxsplit=1)
            period = int(f[1])

            selected = find_way(ways, period)
            display_way(selected)

        elif command.startswith("save "):
            # Разбить команду на части для выделения имени файла.
            f = command.split(maxsplit=1)
            # Получить имя файла.
            file_name = f[1]
            # Сохранить данные в файл с заданным именем.
            save_ways(file_name, ways)

        elif command.startswith("load "):
            # Разбить команду на части для выделения имени файла.
            f = command.split(maxsplit=1)
            # Получить имя файла.
            file_name = f[1]
            # Сохранить данные в файл с заданным именем.
            ways = load_ways(file_name, first_load)

        elif command == 'help':
            # Вывести справку.
            print("Список команд:\n")
            print("add - добавить маршрут;")
            print("list - вывести список маршрутов;")
            print("find - вывод информации о маршруте;")
            print("save - сохранить данные в файл;")
            print("load - загрузить данные из файла;")
            print("help - отобразить справку;")
            print("exit - завершить работу с программой.")

        else:
            print(f"Неизвестная команда {command}", file=sys.stderr)


if __name__ == '__main__':
    main()
