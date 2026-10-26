from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

from tkinter import *
from tkinter import ttk
from tkinter.filedialog import *
from tkinter.messagebox import showwarning, showinfo

# Генерация ключевой пары RSA
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

public_key = private_key.public_key()

# Сохранение ключей RSA в файлы
with open("private_key_3.pem", "wb") as f:
    f.write(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ))

with open("public_key_3.pem", "wb") as f:
    f.write(public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ))

EncryptedMessage = None

# Создание и настройка окна приложения
root = Tk()
root.resizable(width=False, height=False)
root.title("Асимметричное шифрование (RSA)")

# Создание вкладок с помощью виджета Notebook
Tabs = ttk.Notebook(root)
Encrypt_TAB = ttk.Frame(Tabs, padding=2)
Decrypt_TAB = ttk.Frame(Tabs, padding=2)

Tabs.add(Encrypt_TAB, text="Зашифровать")
Tabs.add(Decrypt_TAB, text="Расшифровать")

# Позиционирование вкладок
Tabs.pack(expand=True, fill=BOTH)

# Общий шрифт для использования
GlobalCipherToUse = StringVar()


# Вкладка "Зашифровать"
TextToEncrypt = Label(Encrypt_TAB, text="Текст: ")
TextToEncrypt.grid(row=0, column=0, pady=5, sticky=W)

EntryToEncrypt = Entry(Encrypt_TAB)
EntryToEncrypt.grid(row=0, column=1, pady=5, sticky=EW)

TextToChooseCipher = Label(Encrypt_TAB, text="Шифр: ")
TextToChooseCipher.grid(row=1, column=0, pady=5, sticky=W)

ChooseCipherEnc = ttk.Combobox(
    Encrypt_TAB,
    values=["SHA1", "SHA256", "SHA512"],
    state="readonly",
    textvariable=GlobalCipherToUse
)
ChooseCipherEnc.grid(row=1, column=1)


def EncryptMessage():
    # Объявляем через global переменнную EncryptMessage,
    # для того, чтобы использовать в функции DecryptMessage
    global EncryptedMessage
    MessageToEncrypt = EntryToEncrypt.get()
    CipherToEncrypt = GlobalCipherToUse.get()

    # Проверка на ошибки
    if not MessageToEncrypt or not CipherToEncrypt:
        showwarning(
            title="ВНИМАНИЕ!",
            message="Не все переменные были заполнены!")
        return

    # Через getattr создаём переводим выбор шифра пользователя в объект для использования в public_key.encrypt
    # ChoosenAlgorithm => getattr(hashes, CipherToEncrypt)
    # ChoosenAlgorithm =>  cryptography.hazmat.primitives.hashes.ШИФР
    # print(ChoosenAlgorithm) => <cryptography.hazmat.primitives.hashes.ШИФР
    # object at 0x0000021342571CD0>
    ChoosenAlgorithm = getattr(hashes, CipherToEncrypt)()

    EncryptedMessage = public_key.encrypt(
        MessageToEncrypt.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=ChoosenAlgorithm),
            algorithm=ChoosenAlgorithm,
            label=None
        )
    )
    # Переводим EncryptMessage в более читаемый формат через hex
    EntryToDecryptChange.set(EncryptedMessage.hex())
    showinfo(title="Зашифровано!", message=EncryptedMessage.hex())


ButtonToEncrypt = Button(
    Encrypt_TAB,
    text="Зашифровать",
    command=EncryptMessage)
ButtonToEncrypt.grid(
    row=3,
    column=0,
    columnspan=2,
    rowspan=2,
    pady=5,
    sticky=EW)


# Вкладка "Расшифровать"
TextToDecrypt = Label(Decrypt_TAB, text="Текст: ")
TextToDecrypt.grid(row=0, column=0, pady=5, sticky=W)

# Общее поле в вкладке "Расшифровать", для указания уже зашифрованного
# текста через .set
EntryToDecryptChange = StringVar()
EntryToDecrypt = Entry(
    Decrypt_TAB,
    state="readonly",
    textvariable=EntryToDecryptChange)
EntryToDecrypt.grid(row=0, column=1, pady=5, sticky=EW)

TextToChooseCipherDec = Label(Decrypt_TAB, text="Шифр: ")
TextToChooseCipherDec.grid(row=1, column=0, pady=5, sticky=W)

ChooseCipherDec = ttk.Combobox(
    Decrypt_TAB,
    values=["SHA1", "SHA256", "SHA512"],
    state="readonly",
    textvariable=GlobalCipherToUse
)
ChooseCipherDec.grid(row=1, column=1)


def DecryptMessage():
    CipherToDecrypt = GlobalCipherToUse.get()

    # Проверка на ошибки через if
    if not CipherToDecrypt or EncryptedMessage is None:
        showwarning(
            title="ВНИМАНИЕ!",
            message="Не все переменные были заполнены!")
        return

    # Через getattr создаём переводим выбор шифра пользователя в объект для использования в public_key.encrypt
    # ChoosenAlgorithm => getattr(hashes, CipherToEncrypt)
    # ChoosenAlgorithm =>  cryptography.hazmat.primitives.hashes.ШИФР
    # print(ChoosenAlgorithm) => <cryptography.hazmat.primitives.hashes.ШИФР
    # object at 0x0000021342571CD0>
    ChoosenAlgorithm = getattr(hashes, CipherToDecrypt)()

    # Проверка на ошибки через try except
    try:
        DecryptMessage = private_key.decrypt(
            EncryptedMessage,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=ChoosenAlgorithm),
                algorithm=ChoosenAlgorithm,
                label=None
            )
        )
    except ValueError:
        # ValueError: Decryption failed
        showwarning(title="ВНИМАНИЕ!", message="Шифр не совпадает!")
        return

    DecryptedMessage = DecryptMessage.decode()
    showinfo(title="Расшифровано!", message=DecryptedMessage)


ButtonToDecrypt = Button(
    Decrypt_TAB,
    text="Расшифровать",
    command=DecryptMessage)
ButtonToDecrypt.grid(
    row=3,
    column=0,
    columnspan=2,
    rowspan=2,
    pady=5,
    sticky=EW)

root.mainloop()
