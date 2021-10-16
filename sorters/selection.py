from .common import BaseSorter, swap_values_in


class SelectionSorter(BaseSorter):
    __slots__ = ()

    def __init__(self):
        super().__init__('Selection')

    def sort(self, nums):
        count = len(nums)
        if count < 2:
            return
        for i in range(count-1):
            min_val, swap_with = nums[i], 0
            for j in range(i+1, count):
                if nums[j] < min_val:
                    min_val, swap_with = nums[j], j
            if swap_with > 0:
                swap_values_in(nums, i, swap_with)
