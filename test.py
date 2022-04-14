import unittest
from hypothesis import given
import hypothesis.strategies as st
from HashMapMutable import *


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
        hash.remove(8)
        self.assertEqual(len(hash), 3)


if __name__ == '__main__':
    unittest.main()

