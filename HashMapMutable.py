from typing import Callable, Dict, Union, Iterator, List


class Node:
    def __init__(self, key: Union[int, str, float, None] = None,
                 value: Union[int, str, float, bool, object, None] = None):
        self.key: Union[int, str, float, None] = key
        self.value: Union[int, str, float, bool, object, None] = value


class HashMap:
    empty = Node()

    def __init__(self, hashcode: int = 51):
        self.key_set: List[Union[int, str, float, None]] = []
        # used to store the elements key added to the hash map
        self.data: List[Node] = [self.empty for _ in range(hashcode)]
        # Used to store element nodes
        self.size = hashcode  # table size
        self.len = 0
        self.index = 0

    def __len__(self) -> int:
        return self.len

    def add(self, key: Union[int, str, float, None],
            value: Union[int, str, float, bool, object, None]) -> bool:
        """
        Insert key-value pairs into hash map
        :param key: The key to insert into the hash map
        :param value: element value
        """
        if key in self.key_set:
            for temp in self.data:
                if temp != self.empty and temp.key == key:
                    temp.value = value
                    return True
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
        return False

    def find_in_key_set(self, key: Union[int, str, float,
                                         bool, object, None]) -> bool:
        """
        Find key in key_set list
        :param key:key to find
        :return: find or not
        """
        for i in self.key_set:
            if i == key:
                return True
        return False

    def get(self, key: Union[int, str, float, None]) -> \
            Union[int, str, float, bool, object, None]:
        """
        Find element in hash map by key.
        :param key:element key
        :return:element value response to the input key
        """
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

    def get_hash_value(self, key: Union[int, str, float, None]) -> \
            Union[int, str, float, bool, object, None]:
        """
        Hash by key
        :param key:element key
        :return:hash value
        """
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

    def remove_by_key(self, key: Union[int, str, float, None]) -> bool:
        """
        Delete element in hash map by key
        :param key:element key
        :return:Boolean type for delete success or failure
        """
        hash_value = self.get_hash_value(key)
        if hash_value == -1:
            return False
            # ?????????
        else:
            self.data[hash_value].key = -1
            self.key_set.remove(key)
            self.len = self.len - 1
            return True

    def remove_by_index(self, index: int) -> bool:
        """
        Delete element in hash map by index
        :param index:element key
        :return:Boolean type for delete success or failure
        """
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

    def get_size(self) -> int:
        """
        Element number in hash map.
        :return:number of element in hash map
        """
        size = len(self.key_set)
        return size

    def to_kv_entry_list(self) -> List[Union[int, str,
                                             float, bool, object, None]]:
        """
        list to store all node in hash map
        :return: result List
        """
        result: List[Union[int, str, float, bool, object, None]] = []
        for key in self.key_set:
            result.append(Node(key, self.get(key)))
        return result

    def from_list(self, input_list: List[Union[int, str, float,
                                               bool, object, None]]) -> None:
        """
        add element from list type
        :param input_list:input list
        :return: None
        """
        for k, v in enumerate(input_list):
            self.add(k, v)

    def to_list(self) -> List[Union[int, str, float, bool, object, None]]:
        """
        Transfer hash map into list type
        :return:result list
        """
        result = []
        for key in self.key_set:
            result.append(self.get(key))
        return result

    def from_dict(self, dict: Dict[Union[int, str, float, None],
                                   Union[int, str, float,
                                         bool, object, None]]) -> None:
        """
        add elements from dict type
        :param dict:input dict
        :return: None
        """
        for k, v in dict.items():
            self.add(k, v)

    def to_dict(self) -> Dict[Union[int, str, float, None],
                              Union[int, str, float, bool, object, None]]:
        """
        transfer hash map into dict
        :return: result kvDict
        """
        kvDict: Dict[Union[int, str, float, None],
                     Union[int, str, float, bool, object, None]] = {}
        if self.len == 0:
            return kvDict
        else:
            for temp in self.data:
                if temp != self.empty and temp.key != -1:
                    kvDict[temp.key] = temp.value
        return kvDict

    def map(self, func: Callable[[Union[int, str, float, bool,
                                        object, None]],
                                 Union[int, str, float, bool,
                                       object, None]]) -> None:
        """
        Map element value in hash map with func
        :param func:input function
        :return: None
        """
        for data in self.data:
            if data != self.empty and data.key != -1:
                data.value = func(data.value)

    def mempty(self) -> None:
        """
        The empty element in property monoid, usually called mempty.
        :return: None
        """
        for key in self.key_set:
            self.data[self.get_hash_value(key)] = self.empty
        self.key_set = []
        self.len = 0

    def mconcat(self, a: 'HashMap') -> None:
        """
        Operation in property monoid.
        :param a: input hash map,add it into self
        :return: None
        """
        if a is None:
            return
        for key in a.key_set:
            value = a.get(key)
            self.add(key, value)

    def find_iseven(self) -> List[Union[int, str, float,
                                        bool, object, None]]:
        """
        Find element with even value in hash map.
        :return:list with even number value
        """
        l: List[Union[int, str, float, bool, object, None]] = self.to_list()
        my_list: List[Union[int, str, float, bool, object, None]] = []
        for value in l:
            if type(value) is int or type(value) is float:
                if value % 2 == 0:
                    my_list.append(value)
        return my_list

    def filter(self, function: Callable[[Union[int, str, float,
                                               bool, object, None]], bool]) \
            -> None:
        """
        Filter element with function in hash map.
        :param function: input function
        :return: None
        """
        for data in self.data:
            if data != self.empty and data.key != -1:
                value = data.value
                flag = function(value)
                if not flag:
                    self.key_set.remove(data.key)
                    data.key = -1
                    self.len -= 1

    def reduce(self,
               f: Callable[[int, Union[int, str, float, bool, object, None]],
                           int],
               initial_state: int) -> int:
        """
        Reduce the mapSet to one value.
        :param f: the reduce method
        :param initial_state:result initial_state
        :return:final res
        """
        state = initial_state
        for key in self.key_set:
            value = self.get(key)
            state = f(state, value)
        return state

    def __iter__(self) -> Iterator[Union[int, str, float,
                                         bool, object, None]]:
        """
        To get a iterable object.
        :return: A custom dictionary object
        """
        return iter(self.to_kv_entry_list())

    def __next__(self) -> Union[int, str, float, bool, object, None]:
        """
        To get the next key-value item.
        :return: The next key-value item.
        """
        if self.index >= self.len:
            raise StopIteration("end of hashmap")
        else:
            self.index += 1
            val = self.get(self.key_set[self.index - 1])
            return val
