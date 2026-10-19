# Шифр Цезаря (для текста)
# Это классический пример подстановки, где каждый символ сдвигается на фиксированное число позиций в алфавите. 

import re

# Добавить ввод для пользователя для переменной text и shift

def caesar_encrypt(text, shift):
    encrypted_text = ""
    for char in text:
        """
        The isalpha() method checks if all characters in a given string are alphabetic. 
        It returns True if every character in the string is a letter and False if the string contains any numbers, spaces, or special characters.
        """
        if char.isalpha():
            """
            Python ord() function returns the Unicode code of a given single character. 
            It is a modern encoding standard that aims to represent every character in every language.

            Unicode includes:

            * ASCII characters (first 128 code points)
            * Emojis, currency symbols, accented characters, etc.
            """
            
            # Заменяя латиницу на кирилицу (ord), то тогда всё заработает 
            # https://ru.stackoverflow.com/questions/917609/python-проверить-чтобы-строка-содержала-только-русские-и-латинские-буквы
            # Костыль... Но работает же!
            # test = "Привет"
            
            if re.search(r'[^а-яА-Я]', char):
                # Латиница
                ascii_offset = ord('a') if char.islower() else ord('A')
            else:
                # Кирилица
                ascii_offset = ord('а') if char.islower() else ord('А')
            # ascii_offset = ord('а') if char.islower() else ord('А')
            encrypted_char = chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
            encrypted_text += encrypted_char
        else:
            encrypted_text += char
    return encrypted_text

def caesar_decrypt(encrypted_text, shift):
    return caesar_encrypt(encrypted_text, -shift)

# Пример использования
# text = "Привет, мир!"
# shift = 3
text = input("Текст: ")
shift = int(input("Сдвиг: "))

encrypted = caesar_encrypt(text, shift)
decrypted = caesar_decrypt(encrypted, shift)
print(f"Зашифровано: {encrypted}")
print(f"Расшифровано: {decrypted}")

# Важно: шифр Цезаря легко взломать методом перебора, поэтому для реальной защиты данных он не подходит.


"""
s1 = "HelloWorld"
res1 = s1.isalpha()
print(res1)

s2 = "Hello123"
res2 = s2.isalpha()
print(res2)


Output:
True
False
"""


"""
For example, unicode of 'A' = 65 and '€' = 8364. Let's look at a code example of ord() function:

print(ord('a'))
print(ord('€'))


Output:
97
8364

Explanation:

* ord() function returns the unicode of the character passed to it as an argument.
* unicode of 'a' = 97 and '€' = 8364.


String Length > 1 Causes Error

The ord() function only accepts a single character. 
If the string length is more than 1, a TypeError will be raised.
print(ord('AB'))


Output:
Traceback (most recent call last):
File "/home/f988dfe667cdc9a8e5658464c87ccd18.py", line 6, in 
value1 = ord('AB')
TypeError: ord() expected a character, but string of length 2 found
"""
