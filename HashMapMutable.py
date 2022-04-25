

class Node:
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value


class HashMap(object):
    empty = object()

    def __init__(self, hashcode=51):
        self.key_set = []
        self.data = [self.empty for _ in range(hashcode)]
        self.size = hashcode
        self.len = 0
        self.index = 0

    def __len__(self):
        return self.len

    def add(self, key, value):
        if key in self.key_set:
            for temp in self.data:
                if temp != self.empty and temp.key == key:
                    temp.value = value
                    return
        else:
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
                        self.key_set.append(key)
                        self.len = self.len + 1
                        return True
                    else:
                        i += 1

    def find_in_key_set(self, value):
        for i in self.key_set:
            if i == value:
                return True
        return False

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

    def remove_by_key(self, key):
        hash_value = self.get_hash_value(key)
        if hash_value == -1:
            return False
            # 未找到
        else:
            self.data[hash_value].key = -1
            self.key_set.remove(key)
            self.len = self.len - 1
            return True

    def remove_by_index(self, index):
        if index < self.size:
            key = self.data[index].key
            if key == -1 or self.data[index] == self.empty:
                print("no element")
                return False
            else:
                self.data[index].key = -1
                self.key_set.remove(key)
                self.len = self.len - 1
                return True
        else:
            print("out of bounds")
            return False

    def get_size(self):
        size = len(self.key_set)
        return size

    def to_kv_entry_list(self):
        list = []
        for key in self.key_set:
            list.append(Node(key, self.get(key)))
        return list

    def from_list(self, list):
        for k, v in enumerate(list):
            self.add(k, v)

    def to_list(self):
        list = []
        for key in self.key_set:
            list.append(self.get(key))
        return list

    def from_dict(self, dict):
        for k, v in dict.items():
            self.add(k, v)

    def to_dict(self):
        kvDict = {}
        if self.len is 0:
            return kvDict
        else:
            for temp in self.data:
                if temp != self.empty and temp.key != -1:
                    kvDict[temp.key] = temp.value
        return kvDict

    def map(self, f):
        dict = {}
        for key in self.key_set:
            value = f(self.get(key))
            dict[key] = value
        return dict

    def mempty(self):
        return None

    def mconcat(self, a, b):
        if a is None:
            return b
        if b is None:
            return a
        for key in b.key_set:
            value = b.get(key)
            a.add(key, value)
        return a

    def find_iseven(self):
        list = self.to_list()
        my_list = []
        for value in list:
            if type(value) is int or type(value) is float:
                if value % 2 == 0:
                    my_list.append(value)
        return my_list

    def filter_iseven(self):
        list = self.to_list()
        for value in list:
            if type(value) is int or type(value) is float:
                if value % 2 == 0:
                    list.remove(value)
        return list

    def reduce(self, f, initial_state):
        state = initial_state
        for key in self.key_set:
            value = self.get(key)
            state = f(state, value)
        return state

    def __iter__(self):
        return iter(self.to_kv_entry_list())

    def __next__(self):
        if self.index >= self.len:
            raise StopIteration("end of hashmap")
        else:
            self.index += 1
            val = self.get(self.key_set[self.index - 1])
            return val