import re

def caesar_encrypt(text, shift):
    encrypted_text = ""
    for char in text:
        if char.isalpha():
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
