# Implementation of a hash table (will be used for storing package data):

# Class for individual hash table entry object
class HashTableEntry:
    # Constructor
    def __init__(self, key, value):
        self.key = key
        self.value = value


# Class for hash table data structure
class HashTable:
    # Constructor
    def __init__(self, initial_capacity=10):
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    # Getter to create and retrieve a hash key
    def _get_hash(self, key):
        bucket = int(key) % len(self.table)
        return bucket

    # Method to insert a new package
    def insert(self, key, value):
        hash_key = self._get_hash(key)
        tuple1 = [key, value]

        if self.table[hash_key] is None:
            self.table[hash_key] = list([tuple1])
            return True
        else:
            for pair in self.table[hash_key]:
                if pair[0] == key:
                    pair[1] = tuple1
                    return True
            self.table[hash_key].append(tuple1)
            return True

    # Method to update value at specified hash
    def update(self, key, value):
        hash_key = self._get_hash(key)
        if self.table[hash_key] is not None:
            for pair in self.table[hash_key]:
                if pair[0] == key:
                    pair[1] = value
                    return True
        else:
            print('There was an error with updating on key: ' + key)

    # Getter to retrieve a value from the hash table
    def get(self, key):
        hash_key = self._get_hash(key)
        if self.table[hash_key] is not None:
            for pair in self.table[hash_key]:
                if pair[0] == key:
                    return pair[1]
        return None

    # Method to delete a hash table entry
    def delete(self, key):
        hash_key = self._get_hash(key)

        if self.table[hash_key] is None:
            return False
        for i in range(0, len(self.table[hash_key])):
            if self.table[hash_key][i][0] == key:
                self.table[hash_key].pop(i)
                return True
        return False

