import hashlib
import secrets
import json
import os

DB_FILE = "users.json"

def load_users():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f)

def register(username, password):
    users = load_users()
    
    salt = secrets.token_bytes(32)
    
    password_bytes = password.encode('utf-8')
    hashed_password = hashlib.scrypt(
        password_bytes, 
        salt=salt, 
        n=16384, 
        r=8, 
        p=1, 
        dklen=32
    )
    
    users[username] = {
        "salt": salt.hex(),
        "hash": hashed_password.hex()
    }
    save_users(users)
    print(f"Пользователь '{username}' успешно зарегистрирован.")

def login(username, password):
    users = load_users()
    
    if username not in users:
        print(f"Пользователь '{username}' не найден.")
        return False
        
    stored_salt_hex = users[username]["salt"]
    stored_hash_hex = users[username]["hash"]
    
    salt = bytes.fromhex(stored_salt_hex)
    
    password_bytes = password.encode('utf-8')
    check_hash = hashlib.scrypt(
        password_bytes, 
        salt=salt, 
        n=16384, 
        r=8, 
        p=1, 
        dklen=32
    )
    
    if check_hash.hex() == stored_hash_hex:
        print("Авторизация успешна. Пароль верный.")
        return True
    else:
        print("Ошибка авторизации. Неверный пароль.")
        return False

if __name__ == "__main__":
    print(" Регистрация ")
    register("ivanov", "SuperSecretPassword123")
    register("petrov", "qwerty")
    
    print("\n Проверка (Верный пароль) ")
    login("ivanov", "SuperSecretPassword123")
    
    print("\n Проверка (Неверный пароль) ")
    login("ivanov", "wrongpassword")
    
    print("\n Проверка (Несуществующий юзер) ")
    login("sidorov", "12345")