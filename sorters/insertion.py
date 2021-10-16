from .common import BaseSorter


class InsertionSorter(BaseSorter):
    __slots__ = ()

    def __init__(self):
        super().__init__('Insertion')

    def sort(self, nums):
        count = len(nums)
        if count < 2:
            return
        for i in range(1, count):
            value, j = nums[i], i - 1
            while j >= 0 and nums[j] > value:
                nums[j + 1] = nums[j]
                j -= 1
            must_move_value = nums[i] != value
            if must_move_value:
                # Have to compensate for the last decrement of j
                nums[j + 1] = value
