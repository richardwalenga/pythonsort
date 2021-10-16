from .common import BaseSorter, swap_values_in


class QuickSorter(BaseSorter):
    __slots__ = ()

    def __init__(self):
        super().__init__('Quick')

    def sort(self, nums):
        self.__sort_between_indexes(nums, 0, len(nums)-1)

    def __sort_between_indexes(self, nums, low, high):
        if low < high:
            pivot_index = self.__partition(nums, low, high)
            self.__sort_between_indexes(nums, low, pivot_index-1)
            self.__sort_between_indexes(nums, pivot_index+1, high)

    # Organizes the values between the high and low indexes where the
    # chosen pivot is moved to a new index where all values greater than
    # the pivot are to its right. The new index for the pivot is returned.
    def __partition(self, nums, low, high):
        pivot = nums[high]
        # initialize the index below low because the index is guaranteed
        # to be incremented before the pivot is moved to its new home.
        new_pivot_index = low - 1
        for i in range(low, high):
            if nums[i] <= pivot:
                new_pivot_index += 1
                swap_values_in(nums, new_pivot_index, i)
        # There will always be at least one swap call since if this is the
        # first time, it means every value checked is greater than the pivot.
        new_pivot_index += 1
        swap_values_in(nums, new_pivot_index, high)
        return new_pivot_index
