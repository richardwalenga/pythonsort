from .common import BaseSorter


class MergeSorter(BaseSorter):
    __slots__ = ('small_array_sorter')

    def __init__(self, small_array_sorter):
        super().__init__('Merge')
        self.small_array_sorter = small_array_sorter

    def sort(self, nums):
        count = len(nums)
        if count < 10:
            self.small_array_sorter.sort(nums)
            return

        mid = count // 2
        first, second = nums[0:mid], nums[mid:]
        first_count, second_count = len(first), len(second)
        self.sort(first)
        self.sort(second)
        for i in range(count):
            first_index, second_index = 0, 0
            can_take_first, can_take_second = first_index < first_count, second_index < second_count
            if can_take_first and (not can_take_second or first[first_index] <= second[second_index]):
                nums[i] = first[first_index]
                if first_index < first_count:
                    first_index += 1
            else:
                nums[i] = second[second_index]
                if second_index < second_count:
                    second_index += 1
