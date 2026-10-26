from pathlib import Path

from cryptography.fernet import Fernet

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

from tkinter import *
from tkinter import ttk
from tkinter.filedialog import *
from tkinter.messagebox import showwarning, showinfo

# Генерация ключевой пары RSA
private_key_rsa = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

public_key_rsa = private_key_rsa.public_key()

# Генерация ключа Fernet
KeyFernet = Fernet.generate_key()
CipherSuiteFernet = Fernet(KeyFernet)

# Создание и настройка окна приложения
root = Tk()
root.resizable(width=False, height=False)
root.title("Шифрование файлов")

# Создание вкладок с помощью виджета Notebook
Tabs = ttk.Notebook(root)
Encrypt_TAB = ttk.Frame(Tabs, padding=2)
Decrypt_TAB = ttk.Frame(Tabs, padding=2)

Tabs.add(Encrypt_TAB, text="Зашифровать")
Tabs.add(Decrypt_TAB, text="Расшифровать")

# Позиционирование вкладок
Tabs.pack(expand=True, fill=BOTH)


def askdirectoryfunc():
    PathWhereSavedDirectory.set(askdirectory())


# Общий путь и шрифт для использования
PathWhereSavedDirectory = StringVar()
GlobalCipherToUse = StringVar()


# Вкладка "Зашифровать"
DataToEncrypt = Label(Encrypt_TAB, text="Выбрать директорию:")
DataToEncrypt.grid(row=0, column=0, pady=5, sticky=W)

ButtonToChooseWhatDirToEncrypt = Button(
    Encrypt_TAB, text="Обзор...", command=askdirectoryfunc)
ButtonToChooseWhatDirToEncrypt.grid(row=0, column=1, pady=5, sticky=EW)

TextToChooseCipher = Label(Encrypt_TAB, text="Шифр: ")
TextToChooseCipher.grid(row=1, column=0, pady=5, sticky=W)

ChooseCipherEnc = ttk.Combobox(
    Encrypt_TAB,
    values=["SHA1", "SHA256", "SHA512"],
    state="readonly",
    textvariable=GlobalCipherToUse
)
ChooseCipherEnc.grid(row=1, column=1)


def EncryptData():
    PathWhereEncrypt = PathWhereSavedDirectory.get()
    FileToEncrypt = Path(PathWhereEncrypt) / "secret.txt"
    CipherToEncrypt = GlobalCipherToUse.get()

    # Проверка на ошибки через if elif
    if not PathWhereEncrypt or not CipherToEncrypt:
        showwarning(
            title="ВНИМАНИЕ!",
            message="Не все переменные были заполнены!")
        return
    elif not FileToEncrypt.is_file():
        showwarning(title="ВНИМАНИЕ!", message="Нет файла secret.txt!")
        return

    ChoosenAlgorithm = getattr(hashes, CipherToEncrypt)()

    # Записывем ключи RSA в файлы
    with open(Path(PathWhereEncrypt) / "private_key_4.pem", "wb") as write_priv_key_rsa:
        write_priv_key_rsa.write(private_key_rsa.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))
    with open(Path(PathWhereEncrypt) / "public_key_4.pem", "wb") as write_pub_key_rsa:
        write_pub_key_rsa.write(public_key_rsa.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

    # Взять данные из файла
    with FileToEncrypt.open("rb") as FTED:
        DataFromFileToEncrypt = FTED.read()

    # Шифрование Fernet + RSA:
    # 1. Fernet шифрует файл и записывает его с расшерением .fernet
    # 2. RSA шифрует ключ Fernet и записывает его с расширением .rsa
    EncryptedByFernet = CipherSuiteFernet.encrypt(DataFromFileToEncrypt)
    EncryptedByRSA = public_key_rsa.encrypt(
        KeyFernet,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=ChoosenAlgorithm),
            algorithm=ChoosenAlgorithm,
            label=None
        )
    )
    with open(Path(PathWhereEncrypt) / "secret.fernet", "wb") as EF, open(Path(PathWhereEncrypt) / "secret.rsa", "wb") as ERSA:
        EF.write(EncryptedByFernet)
        ERSA.write(EncryptedByRSA)
    showinfo(
        title="Зашифровано!",
        message="Файл был зашифрован в secret.fernet + secret.rsa")


ButtonToEncrypt = Button(Encrypt_TAB, text="Зашифровать", command=EncryptData)
ButtonToEncrypt.grid(
    row=3,
    column=0,
    columnspan=2,
    rowspan=2,
    pady=5,
    sticky=EW)


# Вкладка "Расшифровать"
DataToDecrypt = Label(Decrypt_TAB, text="Выбрать директорию:")
DataToDecrypt.grid(row=0, column=0, pady=5, sticky=W)

ButtonToChooseWhatDirToDecrypt = Button(
    Decrypt_TAB, text="Обзор...", command=askdirectoryfunc)
ButtonToChooseWhatDirToDecrypt.grid(row=0, column=1, pady=5, sticky=EW)

TextToChooseCipherDec = Label(Decrypt_TAB, text="Шифр: ")
TextToChooseCipherDec.grid(row=1, column=0, pady=5, sticky=W)

ChooseCipherDec = ttk.Combobox(
    Decrypt_TAB,
    values=["SHA1", "SHA256", "SHA512"], 
    state="readonly",
    textvariable=GlobalCipherToUse
)
ChooseCipherDec.grid(row=1, column=1)


def DecryptData():
    PathWhereDecrypt = PathWhereSavedDirectory.get()
    FileToDecrypt = Path(PathWhereDecrypt) / "secret.dec"
    CipherToDecrypt = GlobalCipherToUse.get()

    # Проверка на ошибки через if else
    if not PathWhereDecrypt or not CipherToDecrypt:
        showwarning(
            title="ВНИМАНИЕ!",
            message="Не все переменные были заполнены!")
        return
    elif not (Path(PathWhereDecrypt) / "secret.fernet").is_file() or not (Path(PathWhereDecrypt) / "secret.rsa").is_file():
        showwarning(
            title="ВНИМАНИЕ!",
            message="Нет файла secret.fernet / secret.rsa!")
        return

    ChoosenAlgorithm = getattr(hashes, CipherToDecrypt)()

    # Взять ключи Fernet и RSA из файлов
    with open(Path(PathWhereDecrypt) / "secret.fernet", "rb") as DF, open(Path(PathWhereDecrypt) / "secret.rsa", "rb") as DRSA:
        EncryptedByFernet = DF.read()
        EncryptedByRSA = DRSA.read()

    # Проверка на ошибки через try except
    try:
        DecryptKeyFernet = private_key_rsa.decrypt(
            EncryptedByRSA,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=ChoosenAlgorithm),
                algorithm=ChoosenAlgorithm,
                label=None
            )
        )
    except BaseException:
        showwarning(title="ВНИМАНИЕ!", message="Шифр не совпадает!")
        return

    DecryptedData = Fernet(DecryptKeyFernet).decrypt(EncryptedByFernet)

    with FileToDecrypt.open("wb") as DD:
        DD.write(DecryptedData)
    showinfo(
        title="Расшифровано!",
        message="Файл был расшифрован в secret.dec")


ButtonToDecrypt = Button(Decrypt_TAB, text="Расшифровать", command=DecryptData)
ButtonToDecrypt.grid(
    row=3,
    column=0,
    columnspan=2,
    rowspan=2,
    pady=5,
    sticky=EW)

root.mainloop()
