# Шифр Виженера (для текста с ключом)
# Более сложный полиалфавитный шифр, где каждая буква сдвигается на значение, определяемое соответствующим символом ключа. 

# ОЧЕНЬ костыльно сделано, но ОПЯТЬ ЖЕ! Работает же! (наверное?...)

"""
https://habr.com/ru/articles/140820/
Если верить тому, кто это написал, то по сути, 
просто нужно - скопировать vigenere_encrypt как vigenere_decrypt, 
и исправить в коде один + на -

encrypted_char = chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset) => +shift
decrypted_char = chr((ord(char) - ascii_offset - shift) % 26 + ascii_offset) => -shift

Брал в основу этот код (вставлю только отрывок, т.к. смысл понятен):
def full_encode => go = (dic[v][0]+dic[v][1]) % len(d)
def full_decode => go = (dic[v][0]-dic[v][1]+len(d)) % len(d) 

И как бы, ну вроде работает (я надеюсь на это XD)
"""


import re

def vigenere_encrypt(text, key):
    encrypted_text = ""
    key_index = 0
    for char in text:
        if char.isalpha():
            if re.search(r'[^а-яА-Я]', char):
                # Латиница
                shift = ord(key[key_index % len(key)].lower()) - ord('a')
                ascii_offset = ord('a') if char.islower() else ord('A')
            else:
                # Кирилица
                shift = ord(key[key_index % len(key)].lower()) - ord('а')
                ascii_offset = ord('а') if char.islower() else ord('А')
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
                shift = ord(key[key_index % len(key)].lower()) - ord('a')
                ascii_offset = ord('a') if char.islower() else ord('A')
            else:
                # Кирилица
                shift = ord(key[key_index % len(key)].lower()) - ord('а')
                ascii_offset = ord('а') if char.islower() else ord('А')
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

"""
len() function returns the number of items present in an object. 
It can be used with strings, lists, tuples, dictionaries, sets and other container types to determine their size.

text = "Programming"
print(len(text))

Output:
11



Examples

Example 1: In this example, we use the len() function to find the number of elements in a list, tuple and dictionary.

fruits = ["Apple", "Mango", "Orange", "Grapes"]
print(len(fruits))

numbers = (10, 20, 30, 40)
print(len(numbers))

student = {"name": "Emma", "age": 21, "city": "London"}
print(len(student))

Output:
4
4
3

Explanation:
* len(fruits) returns 4 because the list contains four elements.
* len(numbers) returns 4 because the tuple contains four values.
* len(student) returns 3 because the dictionary contains three key-value pairs.


Example 2: In this example, we use the len() function to find the length of an empty list.

a = []
print(len(a))

Output:
0

Explanation: Since the list is empty, len() returns 0, indicating there are no elements inside it.


Example 3: In this example, we use len() with range() to access and display each element of a list using its index.

a = [10, 20, 30, 40, 50]

for i in range(len(a)):
    print("Index:", i, "Value:", a[i])


Output:
Index: 0 Value: 10
Index: 1 Value: 20
Index: 2 Value: 30
Index: 3 Value: 40
Index: 4 Value: 50

Explanation: 
range() and len() are used to iterate over the list a by index. 
len(a) gives the total number of elements and range(len(a)) provides the index sequence. 
In each iteration, a[i] accesses the value at index i.
"""
