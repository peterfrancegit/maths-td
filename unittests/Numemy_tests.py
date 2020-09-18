import unittest
import pytest
import sys

sys.path.insert(1, './src')

from Numemy import Numemy


class TestTakeDamage(unittest.TestCase):
    def test_add(self):
        numemy = Numemy(None, 10, None, None, None, None)
        numemy.take_damage('+', 10)
        self.assertEqual(numemy.value, 20)


if __name__ == '__main__':
    unittest.main()
