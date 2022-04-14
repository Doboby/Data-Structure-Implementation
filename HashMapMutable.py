class Node:
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value

class HashMap(object):
    empty = object()
    #暂时设置探测因子为1,探测方法为：h(key) = key%13 + 1
    def __init__(self,hashcode=13,dict=None):
        self.key_set = []
        self.data = [self.empty for _ in range(hashcode)]
        self.size = hashcode
        self.len = 0

    def __len__(self):
        return self.len

    def add(self, key, value):

        hash_value = hash(key) % self.size #这里为了解决不仅仅是数字的情形 或许是字符串 元组等
        kv_entry = Node(key, value)

        if self.data[hash_value] == self.empty or self.data[hash_value].key == -1: #想要放的位置正好没有数据 直接放 这里设定empty 或者key值为-1都可以放
            #key值设置-1 是因为删除的时候预防断链
            self.data[hash_value] = kv_entry
            self.key_set.append(key)
            self.len = self.len + 1
        else: #这里没有处理一种情况 就是在key值一样的时候需要替换 所以测试的时候不要给一样的key值：）
            i = 0
            flag = False
            while i < self.size:
                index = (hash_value + 1 ) % self.size  #下一个探测的位置
                hash_value = index
                if self.data[index] == self.empty or self.data[hash_value].key == -1: #检查
                    self.data[index] = kv_entry
                    self.len = self.len + 1
                    flag = True
                    break
                else:
                    hash_value += 1
                    i += 1
            if not flag:
                print("no space") #这里或许要改进 如果没有空间可以扩容

    def get(self, key):
        hash_value = hash(key) % self.size
        j = 0
        while j < self.size:
            if self.data[hash_value] == self.empty: #断链直接返回没找到
                return None
            elif self.data[hash_value].key == key: #找到的位置的key和要找的key匹配
                return self.data[hash_value].value
            else:
                hash_value = (hash_value + 1) % self.size
                j += 1
        print("no element")
        return None

    def get_hash_value(self, key):
        # 这个方法是为了帮助remove方法获得hash_value，方便修改key
        hash_value = hash(key) % self.size
        j = 0
        while j < self.size:
            if self.data[hash_value] == self.empty:  # 断链直接返回没找到
                return -1
            elif self.data[hash_value].key == key:  # 找到的位置的key和要找的key匹配
                return hash_value
            else:
                hash_value = (hash_value + 1) % self.size
                j += 1
        print("no element")
        return -1

    def remove(self, key):#为防止断链，这里将被删元素的key改为-1即可
        hash_value = self.get_hash_value(key)
        if hash_value == -1:
            return False
            # 未找到
        else:
            self.data[hash_value].key = -1
            self.key_set.remove(key)
            self.len = self.len - 1
            return True
            # 找到并将key值置为-1 懒惰删除




