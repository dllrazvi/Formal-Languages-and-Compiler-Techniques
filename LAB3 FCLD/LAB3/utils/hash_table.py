class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(size)]

    def hash(self, key):
        return sum(ord(c) for c in key) % self.size

    def insert(self, key):
        index = self.hash(key)
        bucket = self.table[index]

        for k in bucket:
            if k == key:
                return

        bucket.append(key)

    def lookup(self, key):
        index = self.hash(key)
        bucket = self.table[index]

        for k in bucket:
            if k == key:
                return True
        return False

    def __str__(self):
        return str(self.table)
