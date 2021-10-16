from .common import BaseSorter, swap_values_in


class BubbleSorter(BaseSorter):
    __slots__ = ()

    def __init__(self, name='Bubble'):
        super().__init__(name)

    def sort(self, nums):
        if len(nums) < 2:
            return
        while self.ltr_sort(nums):
            pass

    def ltr_sort(self, nums):
        swapped = False
        for i in range(1, len(nums)):
            if nums[i - 1] > nums[i]:
                swap_values_in(nums, i - 1, i)
                swapped = True
        return swapped


class CocktailShakerSorter(BubbleSorter):
    # By applying a bitmask of 1 less than a power of 2, I can cleanly
    # alternate sorting left to right followed by right to left.
    BITMASK = 1
    __slots__ = ('sort_methods')

    def __init__(self):
        super().__init__('Cocktail Shaker')
        self.sort_methods = [self.ltr_sort, self.rtl_sort]

    def sort(self, nums):
        if len(nums) < 2:
            return
        i = 0
        while True:
            if not self.sort_methods[i](nums):
                break
            i = (i + 1) & self.__class__.BITMASK

    def rtl_sort(self, nums):
        swapped = False
        for i in range(len(nums) - 1, 0, -1):
            if nums[i] < nums[i - 1]:
                swap_values_in(nums, i - 1, i)
                swapped = True
        return swapped
