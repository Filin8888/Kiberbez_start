import bcrypt
import sqlite3

data = sqlite3.connect("data.db")
cursor = data.cursor()

# Створення БД
cursor.execute("" \
    "CREATE TABLE IF NOT EXISTS data(" \
    "id INTEGER PRIMARY KEY, " \
    "user TEXT, " \
    "hesh TEXT)")

data.commit()

# Рефлізація користувацького інтерфейсу
user_email = input("Введіть свій email: ")
user_password = input("Введіть пароль: ").encode()

# Шифрування пароля
hashed = bcrypt.hashpw(user_password, bcrypt.gensalt())
print("Пароль успішно захешовано")


# Додаємо данні в бібліотеку
cursor.execute("INSERT INTO data(user, hesh) VALUES (?, ?)", (user_email, hashed))
data.commit()
print(f"Додано користувача {user_email}")


# Функція для реалізвації входу користувача
def user_entry(cursor):
    user_email = input("Введіть свій email: ")
    cursor.execute("SELECT * FROM data WHERE user = ?", (user_email,))
    result = cursor.fetchone()

    if result:

        attempts = 3
        
        #Повторне введення паролю
        print(f"Користувач з email {user_email} знайдено")

        while attempts > 0:
            password_check = input("Введіть пароль: ").encode()

        #Перевірка хешу
            if bcrypt.checkpw(password_check, result[2]):
                print(f"Особу підтверджено \nВітаємо {user_email}")
                break
            else:
                attempts -= 1
                print(f"Невірний пароль! Залишилось спроб: {attempts}")
                if attempts == 0:
                    print("Забагато невдалих спроб")
                    exit()
            
    else:
        print(f"Користувача {user_email} неіснує")



# Інтерфейс входу
print("Бажаєте увійти?")
while True:
    print("1. Так")
    print("2. Ні")
    # print("3. Зареєструватися")
    choice =input("Ваш вибір: ")

    if choice == "1":
        user_entry(cursor)      
    elif choice == "2":
        break
    else:
        print("Невідома команда")




