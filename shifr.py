import sqlite3
import os
from cryptography.fernet import Fernet as F


#Створення ключa
KEY_FILE = "secret.key"

if os.path.exists(KEY_FILE):
    with open(KEY_FILE, "rb") as f:
        key = f.read()
else:
    key = F.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)

chifr = F(key)


my_data = sqlite3.connect("my_data.db")
cursor = my_data.cursor()

# Створили БД
cursor.execute("" \
"   CREATE TABLE IF NOT EXISTS my_data(" \
"   id INTEGER PRIMARY KEY, " \
"   unit TEXT, " \
"   data BLOB)")
my_data.commit()


# Шифрування інфи як функція
def info_shifr(info: bytes) -> bytes:
    #Шифрує передану інформацію та повертає зашифрований байтовий рядок.
    secret_info = chifr.encrypt(info)
    print("Інформація зашифрована!")
    return secret_info


# Рефлізація користувацького інтерфейсу
user_unit = input("Що ви бажаєте зберегти? \n ")
user_info = input("Введіть бажану інформацію: ")

while True:
    print("Зашифрувати введену інформацію?[Y/N]")
    choice = input("").strip().upper()

    if choice == "Y":
        encrypted_info = info_shifr(user_info.encode())
        cursor.execute("INSERT INTO my_data(unit, data) VALUES (?, ?)", (user_unit, encrypted_info))
        my_data.commit()
        print("✅ Дані зашифровано та збережено.")
        break
    elif choice == "N":
        cursor.execute("INSERT INTO my_data(unit, data) VALUES (?, ?)", (user_unit, user_info))
        my_data.commit()
        print("✅ Дані збережено без шифрування.")
        break
    else:
        print("❌ UNKNOWN COMMAND!!! Спробуйте ще раз.")


# Функція для реалізвації виводу iнформації користувача
def user_entry(cursor):
    user_unit = input("Що ви хочете дізнатися? \n ")
    cursor.execute("SELECT * FROM my_data WHERE unit = ?", (user_unit,))
    result = cursor.fetchone()


    if result:
        try:
            # Розшифрування
            decrypted_info = chifr.decrypt(result[2]).decode()
            print("Отримано збережену інформацію! \n", decrypted_info) 
        except Exception:
            print("Інформація не зашифрована, ось вона:\n", result[2].decode())          
    else:
        print(f"Інформації за запитом {user_unit} неіснує")



# Інтерфейс входу
print("Бажаєте отримати інформацію? [Y/N]")
choice = input("").strip().upper()

if choice == "Y":
    user_entry(cursor)
else:
    exit()

