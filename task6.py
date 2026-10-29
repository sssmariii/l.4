import os
import hashlib

def get_file_hash(filepath):
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def find_duplicates(directory):
    if not os.path.isdir(directory):
        print("Ошибка: указанная директория не существует.")
        return

    hashes = {}
    
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        
        if os.path.isfile(filepath):
            file_hash = get_file_hash(filepath)
            
            if file_hash not in hashes:
                hashes[file_hash] = []
            hashes[file_hash].append(filepath)
            
    found = False
    print("\nРезультат поиска дубликатов:")
    
    for file_hash, paths in hashes.items():
        if len(paths) > 1:
            found = True
            print(f"Хеш: {file_hash}")
            for path in paths:
                print(f"  - {path}")
            print()
            
    if not found:
        print("Дубликаты не найдены.")

if __name__ == "__main__":
    target_path = input("Введите путь до директории: ")
    find_duplicates(target_path)