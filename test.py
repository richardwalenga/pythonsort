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
tosort_nums = [10305, 17829, 2006, 4451, 9215, 29867, 11673, 15716, 32718, 14891, 6134, 17621, 12297, 20414, 25271, 25334, 15818, 14262, 19925, 5898, 9876, 28097, 14935, 13288, 18322, 19375, 28130, 9168, 21761, 19164, 16927, 6963, 21180, 16374, 18165, 15393, 8972, 31301, 1941, 28127, 22404, 16556, 6994, 23000, 10680, 6707, 14938, 9120, 5152, 22219, 15043, 28882, 30818, 7221, 26435, 26363, 27927, 12987, 10943, 32249, 9048, 5378, 23803, 29246, 27413, 23601, 11808, 27628, 31971, 17970, 3859, 15621, 20739, 19678, 9994, 9159, 24451, 8655, 16745, 608, 31720, 19106, 26200, 16238, 1186, 14332, 5711, 18243, 5650, 6100, 4968, 9291, 16037, 27575, 28820, 5035, 18778, 16429, 2725, 32380, 4206, 9696, 6048, 5530, 13907, 11605, 21674, 8736, 27896, 18199, 26215, 1776, 10198, 25176, 8557, 13935, 13824, 17930, 30904, 32677, 11320, 15187, 18866, 21894, 2470, 12264, 26935, 11968, 32201, 14663, 31118, 6569, 23023, 28606, 23429, 10691, 31989, 19764, 5124, 10520, 9142, 8328, 25968, 22589, 10386, 9134, 8554, 29413, 9762, 14193, 3492, 3100, 8650, 23945, 20117, 14553, 16372, 27419, 29540, 18921, 25667, 5374, 23250, 6878, 2564, 6727, 21135, 13237, 14318, 2433, 12979, 10268, 32671, 14523, 1389, 30897, 17119, 30645, 9873, 5664, 19810, 4520, 13484, 3515, 32388, 5288, 14028, 14089, 17832, 10087, 28487, 11920, 2636, 3936, 31316, 13306, 2069, 18239, 7416, 24140]
sorted_nums = [608, 1186, 1389, 1776, 1941, 2006, 2069, 2433, 2470, 2564, 2636, 2725, 3100, 3492, 3515, 3859, 3936, 4206, 4451, 4520, 4968, 5035, 5124, 5152, 5288, 5374, 5378, 5530, 5650, 5664, 5711, 5898, 6048, 6100, 6134, 6569, 6707, 6727, 6878, 6963, 6994, 7221, 7416, 8328, 8554, 8557, 8650, 8655, 8736, 8972, 9048, 9120, 9134, 9142, 9159, 9168, 9215, 9291, 9696, 9762, 9873, 9876, 9994, 10087, 10198, 10268, 10305, 10386, 10520, 10680, 10691, 10943, 11320, 11605, 11673, 11808, 11920, 11968, 12264, 12297, 12979, 12987, 13237, 13288, 13306, 13484, 13824, 13907, 13935, 14028, 14089, 14193, 14262, 14318, 14332, 14523, 14553, 14663, 14891, 14935, 14938, 15043, 15187, 15393, 15621, 15716, 15818, 16037, 16238, 16372, 16374, 16429, 16556, 16745, 16927, 17119, 17621, 17829, 17832, 17930, 17970, 18165, 18199, 18239, 18243, 18322, 18778, 18866, 18921, 19106, 19164, 19375, 19678, 19764, 19810, 19925, 20117, 20414, 20739, 21135, 21180, 21674, 21761, 21894, 22219, 22404, 22589, 23000, 23023, 23250, 23429, 23601, 23803, 23945, 24140, 24451, 25176, 25271, 25334, 25667, 25968, 26200, 26215, 26363, 26435, 26935, 27413, 27419, 27575, 27628, 27896, 27927, 28097, 28127, 28130, 28487, 28606, 28820, 28882, 29246, 29413, 29540, 29867, 30645, 30818, 30897, 30904, 31118, 31301, 31316, 31720, 31971, 31989, 32201, 32249, 32380, 32388, 32671, 32677, 32718]


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
    def __test_sort(self, sorter):
        self.nums = copy.copy(tosort_nums)
        sorter.sort(self.nums)
        self.assertEqual(self.nums, sorted_nums)

    def __test_rand_sort(self, sorter):
        self.nums = copy.copy(random_nums)
        watch = SimpleStopWatch()
        watch.start()
        sorter.sort(self.nums)
        diff = watch.get_elapsed_milliseconds()
        logger.info('Sorting with %s finished in %i milliseconds',
                    sorter.name, diff)
        self.assertTrue(is_sorted(self.nums))

    def test_insertion(self):
        self.__test_sort(insertion_sorter)
        self.__test_rand_sort(insertion_sorter)

    def test_bubble(self):
        bubble_sorter = BubbleSorter()
        self.__test_sort(bubble_sorter)
        self.__test_rand_sort(bubble_sorter)

    def test_cocktail(self):
        cocktail_sorter = CocktailShakerSorter()
        self.__test_sort(cocktail_sorter)
        self.__test_rand_sort(cocktail_sorter)

    def test_heap(self):
        heap_sorter = HeapSorter(insertion_sorter)
        self.__test_sort(heap_sorter)
        self.__test_rand_sort(heap_sorter)

    def test_selection(self):
        selection_sorter = SelectionSorter()
        self.__test_sort(selection_sorter)
        self.__test_rand_sort(selection_sorter)

    def test_merge(self):
        merge_sorter = MergeSorter(insertion_sorter)
        self.__test_sort(merge_sorter)
        self.__test_rand_sort(merge_sorter)

    def test_quick(self):
        quick_sorter = QuickSorter()
        self.__test_sort(quick_sorter)
        self.__test_rand_sort(quick_sorter)


if __name__ == '__main__':
    unittest.main()
