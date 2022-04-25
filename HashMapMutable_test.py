import unittest
from hypothesis import given
import hypothesis.strategies as st
from HashMapMutable import HashMap


class TestHashMapMutable(unittest.TestCase):

    def test_add(self):
        hash = HashMap()
        hash.add(3, 6)
        self.assertEqual(hash.get(3), 6)
        hash.add(16, 5)
        self.assertEqual(hash.get(16), 5)
        hash.add(4, 5)
        self.assertEqual(hash.get(4), 5)

    def test_get(self):
        hash = HashMap()
        hash.add(4, 12)
        hash.add(8, 123)
        hash.add(11, 44)
        hash.add(14, 66)
        self.assertEqual(hash.get(4), 12)
        self.assertEqual(hash.get(8), 123)
        self.assertEqual(hash.get(11), 44)
        self.assertEqual(hash.get(14), 66)

    def test_remove(self):
        hash = HashMap()
        hash.add(4, 12)
        hash.add(8, 123)
        hash.add(11, 44)
        hash.add(14, 66)
        hash.remove_by_key(8)
        self.assertEqual(hash.get_size(), 3)

    def test_from_dict(self):
        hash = HashMap()
        dict = {1: 2, 2: 4, 3: 6, 4: 8}
        hash.from_dict(dict)
        self.assertEqual(hash.get(4), 8)
        self.assertEqual(hash.get(3), 6)

    def test_to_dict(self):
        hash = HashMap()
        hash.add(1, 2)
        hash.add(2, 3)
        hash.add(3, 2)
        hash.add(5, 1)
        hash.to_dict()
        self.assertEqual(hash.to_dict(), {1: 2, 3: 2, 5: 1, 2: 3})

    def test_get_size(self):
        hash = HashMap()
        self.assertEqual(hash.get_size(), 0)
        hash.add(1, 2)
        self.assertEqual(hash.get_size(), 1)
        hash.add(14, 2)
        self.assertEqual(hash.get_size(), 2)
        hash.add(1, 3)
        self.assertEqual(hash.get_size(), 2)

    def test_to_list(self):
        hash = HashMap()
        dict = {4: 2, 3: 2, 5: 1, 1: 3}
        hash.from_dict(dict)
        self.assertEqual(hash.to_list(), [2, 2, 1, 3])

    def test_find_iseven(self):
        hash = HashMap()
        hash.from_list([1, 5, 6.0, 7.0, None, 'ss', 'dasd'])
        self.assertEqual(hash.to_list(), [1, 5, 6.0, 7.0, None, 'ss', 'dasd'])
        self.assertEqual(hash.find_iseven(), [6.0])

    def test_filter_iseven(self):
        hash = HashMap()
        hash.from_list([1, 5, 6.0, 7.0, None, 'ss', 'dasd'])
        self.assertEqual(hash.to_list(), [1, 5, 6.0, 7.0, None, 'ss', 'dasd'])
        self.assertEqual(hash.filter_iseven(), [1, 5, 7.0, None, 'ss', 'dasd'])

    def test_map(self):
        dict1 = {3: 23, 4: 323}
        dict2 = {3: '23', 4: '323'}
        hash = HashMap()
        hash.from_dict(dict1)
        self.assertEqual(hash.map(str), dict2)

    def test_reduce(self):
        hash = HashMap()
        self.assertEqual(hash.reduce(lambda st, e: st + e, 0), 0)
        dict1 = {3: 23, 4: 323}
        hash1 = HashMap()
        hash1.from_dict(dict1)
        self.assertEqual(hash1.reduce(lambda st, e: st + e, 0), 346)

    def test_iter(self):
        dict1 = {1: 123, 2: 333, 3: 23, 4: 323}
        table = HashMap()
        table.from_dict(dict1)
        tmp = {}
        for e in table:
            tmp[e.key] = e.value
        self.assertEqual(table.to_dict(), tmp)
        i = iter(HashMap())
        self.assertRaises(StopIteration, lambda: next(i))

    @given(a=st.lists(st.integers()))
    def test_monoid_identity(self, a):
        hash = HashMap()
        hash_a = HashMap()
        hash_a.from_list(a)
        self.assertEqual(hash.mconcat(hash.mempty(), hash_a), hash_a)
        self.assertEqual(hash.mconcat(hash_a, hash.mempty()), hash_a)

    @given(a=st.lists(st.integers()),
           b=st.lists(st.integers()),
           c=st.lists(st.integers()))
    def test_monoid_associativity(self, a, b, c):
        hash = HashMap()
        hash_a = HashMap()
        hash_b = HashMap()
        hash_c = HashMap()
        # add list to HashMap
        hash_a.from_list(a)
        hash_b.from_list(b)
        hash_c.from_list(c)
        # (a·b)·c
        a_b = hash.mconcat(hash_a, hash_b)
        ab_c = hash.mconcat(a_b, hash_c)
        # a·(b·c)
        b_c = hash.mconcat(hash_b, hash_c)
        a_bc = hash.mconcat(hash_a, b_c)
        self.assertEqual(ab_c, a_bc)

    @given(st.lists(st.integers()))
    def test_from_list_to_list_equality(self, a):
        hash = HashMap()
        hash.from_list(a)
        b = hash.to_list()
        self.assertEqual(a, b)

    @given(st.lists(st.integers()))
    def test_python_len_and_list_size_equality(self, a):
        hash = HashMap()
        hash.from_list(a)
        self.assertEqual(hash.get_size(), len(a))

    @given(st.lists(st.integers()))
    def test_from_list(self, a):
        hash = HashMap()
        hash.from_list(a)
        self.assertEqual(hash.to_list(), a)
