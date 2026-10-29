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

def count_word_occurrences(text):
    ht = HashTable()
    words = text.split()
    result = []
    
    for word in words:
        if word in ht:
            count = ht.get(word)
            count += 1
            ht.put(word, count)
            result.append(str(count))
        else:
            ht.put(word, 1)
            result.append("1")
            
    return " ".join(result)

if __name__ == "__main__":
    input_text = "Раз раз раз как меня слышно Повторяю раз раз раз Повторяю"
    print("Ввод:")
    print(input_text)
    print("\nВывод:")
    print(count_word_occurrences(input_text))