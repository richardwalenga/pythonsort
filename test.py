from sorters.bubble import BubbleSorter, CocktailShakerSorter
from sorters.heap import HeapSorter, HeapStorage
from sorters.insertion import InsertionSorter
from sorters.selection import SelectionSorter
from sorters.merge import MergeSorter
from sorters.quick import QuickSorter
import copy
import datetime as DT
import logging
import random
import sys
import unittest


def is_sorted(nums):
    for i in range(len(nums)-1):
        if nums[i + 1] < nums[i]:
            return False
    return True


class SimpleStopWatch:
    __slots__ = ('started')

    def start(self):
        self.started = DT.datetime.now()

    def get_elapsed_milliseconds(self):
        return (DT.datetime.now() - self.started) // DT.timedelta(milliseconds=1)


logging.basicConfig(stream=sys.stderr, level=logging.INFO)
logger = logging.getLogger(__name__)
insertion_sorter = InsertionSorter()
random_nums = [random.randint(0, 100000) for _ in range(20000)]


class HeapStorageTest(unittest.TestCase):
    def setUp(self):
        self.capacity = 10
        self.storage = HeapStorage(capacity=self.capacity)

    def test_can_expand(self):
        self.storage[self.capacity + 1] = self.capacity
        self.storage[self.capacity + 5] = 2*self.capacity
        self.assertListEqual(
            self.storage[-5:], [self.capacity, None, None, None, 2*self.capacity])

    def test_cannot_alter_first_element(self):
        self.assertEqual(self.storage[0], None)
        with self.assertRaises(IndexError):
            self.storage[0] = 0


class SorterTest(unittest.TestCase):
    def setUp(self):
        self.nums = copy.copy(random_nums)

    def __test_sort(self, sorter):
        watch = SimpleStopWatch()
        watch.start()
        sorter.sort(self.nums)
        diff = watch.get_elapsed_milliseconds()
        logger.info('Sorting with %s finished in %i milliseconds',
                    sorter.name, diff)
        self.assertTrue(is_sorted(self.nums))

    def test_insertion(self):
        self.__test_sort(insertion_sorter)

    def test_bubble(self):
        self.__test_sort(BubbleSorter())

    def test_cocktail(self):
        self.__test_sort(CocktailShakerSorter())

    def test_heap(self):
        self.__test_sort(HeapSorter(insertion_sorter))

    def test_selection(self):
        self.__test_sort(SelectionSorter())

    def test_merge(self):
        self.__test_sort(MergeSorter(insertion_sorter))

    def test_quick(self):
        self.__test_sort(QuickSorter())


if __name__ == '__main__':
    unittest.main()
