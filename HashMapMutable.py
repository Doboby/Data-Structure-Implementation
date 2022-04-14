

class Node:
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value


class HashMap(object):
    empty = object()

    def __init__(self, hashcode=13):
        self.key_set = []
        self.data = [self.empty for _ in range(hashcode)]
        self.size = hashcode
        self.len = 0

    def __len__(self):
        return self.len

    def add(self, key, value):

        hash_value = hash(key) % self.size
        kv_entry = Node(key, value)

        if self.data[hash_value] == self.empty \
                or self.data[hash_value].key == -1:
            self.data[hash_value] = kv_entry
            self.key_set.append(key)
            self.len = self.len + 1
        else:
            i = 0
            flag = False
            while i < self.size:
                index = (hash_value + 1) % self.size
                hash_value = index
                if self.data[index] == self.empty \
                        or self.data[hash_value].key == -1:
                    self.data[index] = kv_entry
                    self.len = self.len + 1
                    flag = True
                    break
                else:
                    hash_value += 1
                    i += 1
            if not flag:
                print("no space")

    def get(self, key):
        hash_value = hash(key) % self.size
        j = 0
        while j < self.size:
            if self.data[hash_value] == self.empty:
                return None
            elif self.data[hash_value].key == key:
                return self.data[hash_value].value
            else:
                hash_value = (hash_value + 1) % self.size
                j += 1
        print("no element")
        return None

    def get_hash_value(self, key):
        hash_value = hash(key) % self.size
        j = 0
        while j < self.size:
            if self.data[hash_value] == self.empty:
                return -1
            elif self.data[hash_value].key == key:
                return hash_value
            else:
                hash_value = (hash_value + 1) % self.size
                j += 1
        print("no element")
        return -1

    def remove(self, key):
        hash_value = self.get_hash_value(key)
        if hash_value == -1:
            return False
            # 未找到
        else:
            self.data[hash_value].key = -1
            self.key_set.remove(key)
            self.len = self.len - 1
            return True




