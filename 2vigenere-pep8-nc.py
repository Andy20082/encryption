import re

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
            encrypted_char = chr(
                (ord(char) - ascii_offset + shift) %
                26 + ascii_offset)
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
            decrypted_char = chr(
                (ord(char) - ascii_offset - shift) %
                26 + ascii_offset)
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
