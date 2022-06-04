import unittest
from typing import Any, Dict, Union
from hypothesis import given
import hypothesis.strategies as st
from HashMapMutable import HashMap

VI = Union[int, str, float, bool, list, dict, object, None, Any]


class TestHashMapMutable(unittest.TestCase):

    def test_add(self) -> None:
        hash = HashMap()
        hash.add(3, 6)
        self.assertEqual(hash.get(3), 6)
        hash.add(16, 5)
        self.assertEqual(hash.get(16), 5)
        hash.add(4, 5)
        self.assertEqual(hash.get(4), 5)

    def test_get(self) -> None:
        hash = HashMap()
        hash.add(4, 12)
        hash.add(8, 123)
        hash.add(11, 44)
        hash.add(14, 66)
        self.assertEqual(hash.get(4), 12)
        self.assertEqual(hash.get(8), 123)
        self.assertEqual(hash.get(11), 44)
        self.assertEqual(hash.get(14), 66)

    def test_remove(self) -> None:
        hash = HashMap()
        hash.add(4, 12)
        hash.add(8, 123)
        hash.add(11, 44)
        hash.add(14, 66)
        hash.remove_by_key(8)
        self.assertEqual(hash.get_size(), 3)

    def test_from_dict(self) -> None:
        hash = HashMap()
        dict1: Dict[int, int] = {1: 2, 2: 4, 3: 6, 4: 8}
        dict2: Dict[str, int] = {"abc": 2, "def": 4, 3: 6, 4: 8}
        hash.from_dict(dict1)
        hash.from_dict(dict2)
        self.assertEqual(hash.get(4), 8)
        self.assertEqual(hash.get(3), 6)

    def test_to_dict(self) -> None:
        hash = HashMap()
        hash.add(1, 2)
        hash.add(2, 3)
        hash.add(3, 2)
        hash.add(5, 1)
        hash.to_dict()
        self.assertEqual(hash.to_dict(), {1: 2, 3: 2, 5: 1, 2: 3})

    def test_get_size(self) -> None:
        hash = HashMap()
        self.assertEqual(hash.get_size(), 0)
        hash.add(1, 2)
        self.assertEqual(hash.get_size(), 1)
        hash.add(14, 2)
        self.assertEqual(hash.get_size(), 2)
        hash.add(1, 3)
        self.assertEqual(hash.get_size(), 2)

    def test_to_list(self) -> None:
        hash = HashMap()
        dict = {4: 2, 3: 2, 5: 1, 1: 3}
        hash.from_dict(dict)
        self.assertEqual(hash.to_list(), [2, 2, 1, 3])

    def test_find_iseven(self) -> None:
        hash = HashMap()
        hash.from_list([1, 5, 6.0, 7.0, None, 'ss', 'dasd'])
        self.assertEqual(hash.to_list(), [1, 5, 6.0, 7.0, None, 'ss', 'dasd'])
        self.assertEqual(hash.find_iseven(), [6.0])

    def test_filter(self) -> None:
        def even(value: int) -> bool:
            if type(value) is int or type(value) is float:
                if value % 2 == 0:
                    return False
            return True
        hash = HashMap()
        hash.from_list([1, 5, 6.0, 7.0, None, 'ss', 'dasd'])
        self.assertEqual(hash.to_list(), [1, 5, 6.0, 7.0, None, 'ss', 'dasd'])
        hash.filter(even)
        self.assertEqual(hash.to_list(), [1, 5, 7.0, None, 'ss', 'dasd'])

    def test_map(self) -> None:
        dict1 = {3: 23, 4: 323}
        dict2 = {3: '23', 4: '323'}
        hash = HashMap()
        hash.from_dict(dict1)
        hash.map(str)
        self.assertEqual(hash.to_dict(), dict2)

    def test_reduce(self) -> None:
        hash = HashMap()
        self.assertEqual(hash.reduce(lambda st, e: st + e, 0), 0)
        dict1 = {3: 23, 4: 323}
        hash1 = HashMap()
        hash1.from_dict(dict1)
        self.assertEqual(hash1.reduce(lambda st, e: st + e, 0), 346)

    def test_iter(self) -> None:
        dict1 = {1: 123, 2: 333, 3: 23, 4: 323}
        table = HashMap()
        table.from_dict(dict1)
        tmp = {}
        for e in table:
            tmp[e.key] = e.value
        self.assertEqual(table.to_dict(), tmp)
        i = iter(HashMap())
        self.assertRaises(StopIteration, lambda: next(i))

    @given(st.lists(st.integers()))
    def test_from_list_to_list_equality(self, a: VI) -> None:
        hash = HashMap()
        hash.from_list(a)
        b = hash.to_list()
        self.assertEqual(a, b)

    @given(st.lists(st.integers()))
    def test_python_len_and_list_size_equality(self, a: VI) -> None:
        hash = HashMap()
        hash.from_list(a)
        self.assertEqual(hash.get_size(), len(a))

    @given(st.lists(st.integers()))
    def test_from_list(self, a: VI) -> None:
        hash = HashMap()
        hash.from_list(a)
        self.assertEqual(hash.to_list(), a)

    @given(a=st.lists(st.integers()))
    def test_monoid_identity(self, a: VI) -> None:
        hash = HashMap()
        hash.mempty()

        hash_a = HashMap()
        hash_a.from_list(a)
        # a·empty
        hash_a.mconcat(hash)
        # empty·a
        hash.mconcat(hash_a)
        self.assertEqual(hash_a.to_list(), hash.to_list())

    @given(a=st.lists(st.integers()),
           b=st.lists(st.integers()), c=st.lists(st.integers()))
    def test_monoid_associativity(self, a: VI,
                                  b: VI, c: VI) -> None:

        hash_a_1 = HashMap()
        hash_a_2 = HashMap()
        hash_b = HashMap()
        hash_c = HashMap()

        hash_a_1.from_list(a)
        hash_a_2.from_list(a)
        hash_b.from_list(b)
        hash_c.from_list(c)

        # (a·b)·c
        hash_a_1.mconcat(hash_b)
        hash_a_1.mconcat(hash_c)
        # a·(b·c)
        hash_b.mconcat(hash_c)
        hash_a_2.mconcat(hash_b)

        self.assertEqual(hash_a_1.to_list(), hash_a_2.to_list())

    @given(a=st.lists(st.integers()))
    def test_empty(self, a: VI) -> None:
        hash = HashMap()
        hash.from_list(a)
        hash.mempty()
        self.assertEqual(hash.to_list(), [])
