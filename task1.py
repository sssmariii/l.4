def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def next_prime(n):
    while not is_prime(n):
        n += 1
    return n

_EMPTY = object()
_DELETED = object()

class HashTable:
    def __init__(self, initial_size=11):
        self.size = next_prime(initial_size)
        self.table = [_EMPTY] * self.size
        self.count = 0

    def _hash(self, key):
        return hash(key) % self.size

    # 1. Квадратичное пробирование
    def _probe(self, key):
        h = self._hash(key)
        for i in range(self.size):
            yield (h + i**2) % self.size

    def _insert(self, key, value):
        first_deleted = None
        for index in self._probe(key):
            if self.table[index] is _EMPTY:
                target = first_deleted if first_deleted is not None else index
                self.table[target] = (key, value)
                self.count += 1
                return
            elif self.table[index] is _DELETED:
                if first_deleted is None:
                    first_deleted = index
            elif self.table[index][0] == key:
                self.table[index] = (key, value)
                return
                
        if first_deleted is not None:
            self.table[first_deleted] = (key, value)
            self.count += 1

    # 4. Метод put с увеличением 
    def put(self, key, value):
        self._insert(key, value)
        if self.count / self.size > 0.7:
            self._resize(next_prime(self.size * 2))

    def _resize(self, new_size):
        old_table = self.table
        self.size = new_size
        self.table = [_EMPTY] * self.size
        self.count = 0
        for item in old_table:
            if item is not _EMPTY and item is not _DELETED:
                self._insert(item[0], item[1])

    def get(self, key):
        for index in self._probe(key):
            if self.table[index] is _EMPTY:
                raise KeyError(key)
            elif self.table[index] is not _DELETED and self.table[index][0] == key:
                return self.table[index][1]
        raise KeyError(key)

    # 2. Функция len()
    def __len__(self):
        return self.count

    # 3. Оператор in
    def __contains__(self, key):
        for index in self._probe(key):
            if self.table[index] is _EMPTY:
                return False
            elif self.table[index] is not _DELETED and self.table[index][0] == key:
                return True
        return False

    # 5. Оператор del с уменьшением
    def __delitem__(self, key):
        for index in self._probe(key):
            if self.table[index] is _EMPTY:
                raise KeyError(key)
            elif self.table[index] is not _DELETED and self.table[index][0] == key:
                self.table[index] = _DELETED
                self.count -= 1
                
                if self.size > 11 and (self.count / self.size) < 0.2:
                    self._resize(next_prime(self.size // 2))
                return
        raise KeyError(key)


#тестирование
if __name__ == "__main__":
    ht = HashTable()
    print(f"Стартовый размер: {ht.size}")

    print("\n Тест п.4: put и ресайз при > 0.7 ")
    for i in range(10):
        ht.put(f"key_{i}", i)
        print(f"Добавлен key_{i}, размер: {ht.size}, элементов: {len(ht)}")

    print("\n Тест п.2: len() ")
    print(f"Элементов: {len(ht)}")

    print("\n Тест п.3: in ")
    print(f"'key_5' в таблице? {'key_5' in ht}")
    print(f"'key_99' в таблице? {'key_99' in ht}")

    print("\n Тест п.1: Квадратичное пробирование ")
    print(f"Поиск 'key_5' через get(): {ht.get('key_5')}")

    print("\nТест п.5: del и ресайз при < 0.2 ")
    for i in range(8):
        del ht[f"key_{i}"]
        print(f"Удален key_{i}, размер: {ht.size}, элементов: {len(ht)}")

    print("\n Итоговая проверка")
    print(f"'key_1' в таблице? {'key_1' in ht}")
    print(f"'key_8' в таблице? {'key_8' in ht}")