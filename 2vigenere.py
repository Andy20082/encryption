# Шифр Виженера (для текста с ключом)
# Более сложный полиалфавитный шифр, где каждая буква сдвигается на значение, определяемое соответствующим символом ключа. 

import re
"""
Модуль re — это встроенная библиотека Python, предоставляющая инструментарий для работы с регулярными выражениями (regular expressions, regex).
Регулярные выражения представляют собой специальный язык шаблонов, который позволяет описывать и находить последовательности символов в тексте.
"""

# Объяснения с encrypt и decrypt
"""
Метод isalpha() проверяет, содержит ли строка только буквенные символы. 
Он возвращает значение True, если каждый символ в строке является буквой, и значение False, 
если строка содержит какие-либо цифры, пробелы или специальные символы.
"""

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

"""
len():
Функция len() — это встроенная функция, которая подсчитывает количество элементов в разных типах данных. 
Например, с её помощью можно быстро узнать, сколько букв в слове «программирование» или сколько чисел в списке [1, 2, 3, 4, 5]. 

text = "Programming"
print(len(text)) # 11
"""

def vigenere_encrypt(text, key):
    encrypted_text = ""
    key_index = 0
    for char in text:
        if char.isalpha():
            if re.search(r'[^а-яА-Я]', char):
                # Латиница
                shift = ord(key[key_index % len(key)].lower()) - ord("a")
                ascii_offset = ord("a") if char.islower() else ord("A")
            else:
                # Кирилица
                shift = ord(key[key_index % len(key)].lower()) - ord("а")
                ascii_offset = ord("а") if char.islower() else ord("А")
            encrypted_char = chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
            encrypted_text += encrypted_char
        else:
            encrypted_text += char
        key_index += 1
    return encrypted_text

def vigenere_decrypt(text, key):
    decrypted_text = ""
    key_index = 0
    for char in text:
        if char.isalpha():
            if re.search(r'[^а-яА-Я]', char):
                # Латиница
                shift = ord(key[key_index % len(key)].lower()) - ord("a")
                ascii_offset = ord("a") if char.islower() else ord("A")
            else:
                # Кирилица
                shift = ord(key[key_index % len(key)].lower()) - ord("а")
                ascii_offset = ord("а") if char.islower() else ord("А")
            decrypted_char = chr((ord(char) - ascii_offset - shift) % 26 + ascii_offset)
            decrypted_text += decrypted_char
        else:
            decrypted_text += char
        key_index += 1
    return decrypted_text

text = input("Текст: ")
key = input("Ключ: ")
encrypted = vigenere_encrypt(text, key)
decrypted = vigenere_decrypt(encrypted, key)
print(f"Зашифровано: {encrypted}")
print(f"Расшифровано: {decrypted}")
