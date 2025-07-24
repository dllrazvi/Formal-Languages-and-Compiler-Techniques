from hash_table import HashTable
from pair import Pair

class SymbolTable:
    def __init__(self, size=100):
        self.table = HashTable(size)

    def get_size(self):
        return self.table.size

    def find_position_of_term(self, term):
        hash_value = self.table.hash(term)
        bucket = self.table.table[hash_value]

        if not bucket:
            return None

        for index, key in enumerate(bucket):
            if key == term:
                return Pair(hash_value, index)

        return None

    def find_by_pos(self, pos):
        if pos is None:
            return None

        bucket = self.table.table[pos.first]
        if 0 <= pos.second < len(bucket):
            return bucket[pos.second]
        return None

    def contains_term(self, term):
        return self.table.lookup(term)

    def add(self, term):
        if not self.contains_term(term):
            self.table.insert(term)

    def __str__(self):
        return str(self.table)
