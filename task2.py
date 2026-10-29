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

class Node:
    def __init__(self, initdata):
        self.data = initdata
        self.next = None

    def getData(self):
        return self.data

    def getNext(self):
        return self.next

    def setData(self, newdata):
        self.data = newdata

    def setNext(self, newnext):
        self.next = newnext

class UnorderedList:
    def __init__(self):
        self.head = None

    def isEmpty(self):
        return self.head == None

    def add(self, item):
        temp = Node(item)
        temp.setNext(self.head)
        self.head = temp

    def size(self):
        current = self.head
        count = 0
        while current != None:
            count = count + 1
            current = current.getNext()
        return count


class HashTable:
    def __init__(self, initial_size=11):
        self.size = next_prime(initial_size)
        # 1. Метод цепочек
        self.table = [UnorderedList() for _ in range(self.size)]
        self.count = 0

    def _hash(self, key):
        return hash(key) % self.size

    # 4. Метод put с автоувеличением (> 0.7)
    def put(self, key, value):
        index = self._hash(key)
        bucket = self.table[index]
        
        current = bucket.head
        while current is not None:
            k, v = current.getData()
            if k == key:
                current.setData((key, value)) 
                return
            current = current.getNext()
            

        bucket.add((key, value))
        self.count += 1

       
        if self.count / self.size > 0.7:
            self._resize(next_prime(self.size * 2))

    def get(self, key):
        index = self._hash(key)
        bucket = self.table[index]
        current = bucket.head
        while current is not None:
            k, v = current.getData()
            if k == key:
                return v
            current = current.getNext()
        raise KeyError(key)

    # 5. Метод del с автоуменьшением (< 0.2)
    def __delitem__(self, key):
        index = self._hash(key)
        bucket = self.table[index]
        current = bucket.head
        previous = None

        while current is not None:
            k, v = current.getData()
            if k == key:
                if previous is None:
                    bucket.head = current.getNext()
                else:
                    previous.setNext(current.getNext())
                self.count -= 1
                
                
                if self.size > 11 and (self.count / self.size) < 0.2:
                    self._resize(next_prime(self.size // 2))
                return
            previous = current
            current = current.getNext()
        raise KeyError(key)

    # 2. Функция len()
    def __len__(self):
        return self.count

    # 3. Оператор in
    def __contains__(self, key):
        index = self._hash(key)
        bucket = self.table[index]
        current = bucket.head
        while current is not None:
            k, v = current.getData()
            if k == key:
                return True
            current = current.getNext()
        return False

    
    def _resize(self, new_size):
        old_table = self.table
        self.size = new_size
        self.table = [UnorderedList() for _ in range(self.size)]
        self.count = 0

        
        for bucket in old_table:
            current = bucket.head
            while current is not None:
                k, v = current.getData()
                self.put(k, v)
                current = current.getNext()

#тестирование

if __name__ == "__main__":
    ht = HashTable()
    print(f"Стартовый размер таблицы: {ht.size}")

    print("\n Тест п.1: Разрешение коллизий (Метод цепочек) ")
    print(f"Тип данных в ячейке таблицы: {type(ht.table[0]).__name__}")

    print("\n Тест п.4: put и ресайз при Load Factor > 0.7 ")
    for i in range(10):
        ht.put(f"key_{i}", i)
        print(f"Добавлен key_{i}, размер: {ht.size}, элементов: {len(ht)}")

    print("\n Тест п.2: len() ")
    print(f"Количество элементов через len(ht): {len(ht)}")

    print("\n Тест п.3: in ")
    print(f"'key_5' в таблице? {'key_5' in ht}")
    print(f"'key_99' в таблице? {'key_99' in ht}")

    print("\n Тест п.5: del и ресайз при Load Factor < 0.2 ")
    for i in range(8):
        del ht[f"key_{i}"]
        print(f"Удален key_{i}, размер: {ht.size}, элементов: {len(ht)}")

    print("\n Итоговая проверка ")
    print(f"'key_1' в таблице? {'key_1' in ht}")
    print(f"'key_8' в таблице? {'key_8' in ht}")