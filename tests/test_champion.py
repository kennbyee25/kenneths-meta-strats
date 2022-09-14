from unittest import TestCase

from champion import Champion


class TestChampion(TestCase):
    def test_toString(self):
        champion = Champion()

        self.assertIsInstance(champion.__str__(), str)
