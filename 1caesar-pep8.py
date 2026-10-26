# Шифр Цезаря (для текста)
# Это классический пример подстановки, где каждый символ сдвигается на фиксированное число позиций в алфавите.
# Важно: шифр Цезаря легко взломать методом перебора, поэтому для реальной
# защиты данных он не подходит.

import re
"""
Модуль re — это встроенная библиотека Python, предоставляющая инструментарий для работы с регулярными выражениями (regular expressions, regex).
Регулярные выражения представляют собой специальный язык шаблонов, который позволяет описывать и находить последовательности символов в тексте.
"""


def caesar_encrypt(text, shift):
    encrypted_text = ""
    for char in text:
        """
        Метод isalpha() проверяет, содержит ли строка только буквенные символы.
        Он возвращает значение True, если каждый символ в строке является буквой, и значение False,
        если строка содержит какие-либо цифры, пробелы или специальные символы.
        """
        if char.isalpha():
            """
            re.search:
            ^ => начало строки
            а-яА-Я => от а до я + от А до Я
            """

            """
            ord():
            Принимает на вход строку из одного символа и возвращает ее порядковый номер в Unicode.
            Важно: ord() выдаст исключение, если строка пуста или содержит больше одного символа.
            """

            """
            chr():
            Функция, выполняющая обратное действие по отношению к ord().
            Принимает на вход число, которое представляет код символа в Unicode, и возвращает соответствующий символ.
            При попытке передать отрицательное число или неправильный тип данных будет вызвано исключение.
            """
            if re.search(r'[^а-яА-Я]', char):
                # Латиница
                ascii_offset = ord("a") if char.islower() else ord("A")
            else:
                # Кирилица
                ascii_offset = ord("а") if char.islower() else ord("А")
            encrypted_char = chr(
                (ord(char) - ascii_offset + shift) %
                26 + ascii_offset)
            encrypted_text += encrypted_char
        else:
            encrypted_text += char
    return encrypted_text


def caesar_decrypt(encrypted_text, shift):
    return caesar_encrypt(encrypted_text, -shift)


text = input("Текст: ")
shift = int(input("Сдвиг: "))

encrypted = caesar_encrypt(text, shift)
decrypted = caesar_decrypt(encrypted, shift)
print(f"Зашифровано: {encrypted}")
print(f"Расшифровано: {decrypted}")
