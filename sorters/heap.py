from .common import BaseSorter
import enum


class EmptyHeapError(Exception):
    pass


class HeapStorageCapacityTooSmallError(Exception):
    pass


class HeapifyDirection(enum.Enum):
    DOWN = 0
    UP = 1


# To make the implementation of the heap more convenient, this
# list will expand to accommodate an assignment out of range.
# The first element is always meant to be empty to make the
# calculations of the parent and child nodes easier.
class HeapStorage(list):
    __slots__ = ()
    ROOT_INDEX = 1

    def __init__(self, capacity):
        if capacity < 5:
            raise HeapStorageCapacityTooSmallError()
        super().__init__((None for _ in range(capacity+1)))

    def __setitem__(self, key, value):
        if key == 0:
            raise IndexError('Cannot assign to first element')
        try:
            super().__setitem__(key, value)
        except IndexError:
            slots_to_add = key - len(self) + 1
            if slots_to_add == 1:
                self.append(value)
                return

            def extension():
                for _ in range(slots_to_add - 1):
                    yield None
                yield value
            self.extend(extension())


class HeapNode:
    __slots__ = ('is_root', 'heap', 'index')

    def __init__(self, heap, index):
        self.is_root = index == HeapStorage.ROOT_INDEX
        self.heap = heap
        self.index = index

    @property
    def value(self):
        return self.heap.storage[self.index]

    @value.setter
    def value(self, new_val):
        self.heap.storage[self.index] = new_val

    def heapify_down(self):
        left, right = self.left(), self.right()
        if left is None and right is None:
            return

        node = right
        if left is not None and right is not None:
            # Favor the smallest or largest child node as a swap partner
            # depending on if one is working with a min or max heap.
            # The comparer will return true if the first value meets this
            # criteria.
            if self.heap.comparer(left.value, right.value):
                node = left
        elif left is not None:
            node = left
        self.try_swap_value_with(node, HeapifyDirection.DOWN)

    def heapify_up(self):
        parent = self.parent()
        if parent is not None:
            self.try_swap_value_with(parent, HeapifyDirection.UP)

    def left(self):
        return self.__from_index(2 * self.index)

    def right(self):
        return self.__from_index(2 * self.index + 1)

    def parent(self):
        return None if self.is_root else HeapNode(self.heap, self.index // 2)

    def __from_index(self, index):
        return None if self.heap.is_out_of_range(index) else HeapNode(self.heap, index)

    def try_swap_value_with(self, other, direction):
        if other is None:
            return

        val, other_val = self.value, other.value
        if direction == HeapifyDirection.DOWN and self.heap.comparer(other_val, val):
            self.value = other_val
            other.value = val
            other.heapify_down()
        elif direction == HeapifyDirection.UP and self.heap.comparer(val, other_val):
            self.value = other_val
            other.value = val
            other.heapify_up()


class Heap:
    __slots__ = ('storage', 'comparer', '__size')

    def __init__(self, is_min=True, capacity=30):
        self.storage = HeapStorage(capacity)

        def min_comparer(x, y):
            return x < y

        def max_comparer(x, y):
            return x > y
        self.comparer = min_comparer if is_min else max_comparer
        self.__size = 0

    def is_out_of_range(self, index):
        return index > self.__size

    def peek(self):
        return self.storage[HeapStorage.ROOT_INDEX] if self.__size > 0 else None

    def store(self, num):
        self.__size += 1
        self.storage[self.__size] = num
        setting_root = self.__size == HeapStorage.ROOT_INDEX
        if not setting_root:
            HeapNode(self, self.__size).heapify_up()

    def take(self):
        if self.__size == 0:
            raise EmptyHeapError()
        # Choosing the last value to temporarily put in the root is
        # arbitrary but requires no extra processing time other than
        # what it takes to let it settle into its new position
        taken = self.storage[HeapStorage.ROOT_INDEX]
        self.storage[HeapStorage.ROOT_INDEX] = self.storage[self.__size]
        self.__size -= 1
        if self.__size > 1:
            HeapNode(self, HeapStorage.ROOT_INDEX).heapify_down()
        return taken


class HeapSorter(BaseSorter):
    __slots__ = ('small_array_sorter')

    def __init__(self, small_array_sorter):
        super().__init__('Heap')
        self.small_array_sorter = small_array_sorter

    def sort(self, nums):
        count = len(nums)
        if count < 10:
            self.small_array_sorter.sort(nums)
            return
        heap = Heap(capacity=count)
        for num in nums:
            heap.store(num)
        for i in range(count):
            nums[i] = heap.take()
