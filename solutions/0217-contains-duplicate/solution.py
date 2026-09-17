class Solution(object):
    def containsDuplicate(self, nums):
        """
        :type nums: List[int]
        :rtype: bool
        """
        
        """

        Given an array "nums" if a value appears twice then return true.
        False if every single element is unique/distinct

        Store a temporary data structure and add to it as we loop through nums
        If the number we already have in the data structure appears once more, then return false

        Differnet methologies:

        -we can do a nested for loop, and basically check everything in O(n^2) time
        -we can do sorting, which is O(nlogn) time 
        -We can do a hashset, which is O(1) look up time, so our final answer will be O(n)

        """

        seen = set()

        for i in range(len(nums)):
            if nums[i] in seen: 
                return True
            seen.add(nums[i])
        return False