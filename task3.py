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

class HashTable:
    def __init__(self, initial_size=11):
        self.size = next_prime(initial_size)
        self.table = [UnorderedList() for _ in range(self.size)]
        self.count = 0

    def _hash(self, key):
        if isinstance(key, str):
            hash_val = 0
            for char in key:
                hash_val = (hash_val * 31 + ord(char)) % self.size
            return hash_val
        return hash(key) % self.size

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

    def __len__(self):
        return self.count

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

# Тестирование строковых ключей
if __name__ == "__main__":
    ht = HashTable()
    print(f"Стартовый размер: {ht.size}")

    print("\n Тест: добавление строковых ключей ")
    words = ["apple", "banana", "cherry", "date", "elderberry", "fig", "grape", "honeydew", "kiwi"]
    for i, word in enumerate(words):
        ht.put(word, i)
        print(f"Добавлен '{word}', размер: {ht.size}, элементов: {len(ht)}")

    print("\n Тест: поиск строковых ключей ")
    print(f"'apple' в таблице? {'apple' in ht}")
    print(f"'watermelon' в таблице? {'watermelon' in ht}")
    print(f"Значение для 'cherry': {ht.get('cherry')}")

    print("\n Тест: удаление строкового ключа ")
    del ht["banana"]
    print(f"'banana' в таблице? {'banana' in ht}")
    print(f"Размер: {ht.size}, элементов: {len(ht)}")